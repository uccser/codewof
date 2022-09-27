////////////////////////////////
// Setup
////////////////////////////////

// Gulp and package
const { src, dest, parallel, series, watch } = require('gulp')
const pjson = require('./package.json')

// Plugins
const autoprefixer = require('autoprefixer')
const browserify = require('browserify')
const buffer = require('vinyl-buffer');
const c = require('ansi-colors')
const concat = require('gulp-concat')
const cssnano = require('cssnano')
const errorHandler = require('gulp-error-handle')
const filter = require('gulp-filter')
const gulpif = require('gulp-if');
const { hideBin } = require('yargs/helpers')
const imagemin = require('gulp-imagemin')
const log = require('fancy-log')
const pixrem = require('pixrem')
const postcss = require('gulp-postcss')
const postcssFlexbugFixes = require('postcss-flexbugs-fixes')
const sass = require('gulp-sass')(require('sass'));
const sourcemaps = require('gulp-sourcemaps')
const tap = require('gulp-tap')
const terser = require('gulp-terser')
const yargs = require('yargs/yargs')

// Arguments
const argv = yargs(hideBin(process.argv)).argv
const PRODUCTION = !!argv.production;

// Relative paths function
function pathsConfig(appName) {
    this.app = `./${pjson.name}`
    const vendorsRoot = 'node_modules'
    const staticSourceRoot = 'static'
    const staticOutputRoot = 'build'

    return {
        app: this.app,
        // Source files
        bootstrap_source: `${vendorsRoot}/bootstrap/scss`,
        css_source: `${staticSourceRoot}/css`,
        scss_source: `${staticSourceRoot}/scss`,
        images_source: `${staticSourceRoot}/img`,
        svg_source: `${staticSourceRoot}/svg`,
        js_source: `${staticSourceRoot}/js`,
        vendor_js_source: [
            `${vendorsRoot}/jquery/dist/jquery.js`,
            `${vendorsRoot}/popper.js/dist/umd/popper.js`,
            `${vendorsRoot}/bootstrap/dist/js/bootstrap.js`,
            `${vendorsRoot}/details-element-polyfill/dist/details-element-polyfill.js`,
        ],
        // Output files
        css_output: `${staticOutputRoot}/css`,
        fonts_output: `${staticOutputRoot}/fonts`,
        images_output: `${staticOutputRoot}/img`,
        svg_output: `${staticOutputRoot}/svg`,
        js_output: `${staticOutputRoot}/js`,
    }
}

var paths = pathsConfig()

function catchError(error) {
    log.error(
        c.bgRed('Error:'),
        c.red(error)
    );
    this.emit('end');
}

////////////////////////////////
// Config
////////////////////////////////

// CSS/SCSS
const processCss = [
    autoprefixer(),         // adds vendor prefixes
    pixrem(),               // add fallbacks for rem units
    postcssFlexbugFixes(),  // adds flexbox fixes
]
const minifyCss = [
    cssnano({ preset: 'default' })   // minify result
]

// JS

const js_files_skip_optimisation = [
    // Optimise all files
    '**',
    // But skip the following files
    // For example: '!static/js/vendor/**/*.js'
];

////////////////////////////////
// Tasks
////////////////////////////////

// Styles autoprefixing and minification
function css() {
    return src(`${paths.css_source}/**/*.css`)
        .pipe(errorHandler(catchError))
        .pipe(sourcemaps.init())
        .pipe(postcss(processCss))
        .pipe(sourcemaps.write())
        .pipe(gulpif(PRODUCTION, postcss(minifyCss))) // Minifies the result
        .pipe(dest(paths.css_output))
}

function scss() {
    return src(`${paths.scss_source}/**/*.scss`)
        .pipe(errorHandler(catchError))
        .pipe(sourcemaps.init())
        .pipe(sass({
            includePaths: [
                paths.bootstrap_source,
                paths.scss_source
            ],
            sourceComments: !PRODUCTION,
        }).on('error', sass.logError))
        .pipe(postcss(processCss))
        .pipe(sourcemaps.write())
        .pipe(gulpif(PRODUCTION, postcss(minifyCss))) // Minifies the result
        .pipe(dest(paths.css_output))
}

// Javascript
function js() {
    const js_filter = filter(js_files_skip_optimisation, { restore: true })
    return src([
        `${paths.js_source}/**/*.js`,
        `!${paths.js_source}/modules/**/*.js`
    ])
        .pipe(errorHandler(catchError))
        .pipe(sourcemaps.init())
        .pipe(js_filter)
        .pipe(tap(function (file) {
            file.contents = browserify(file.path, { debug: true }).bundle().on('error', catchError);
        }))
        .pipe(buffer())
        .pipe(gulpif(PRODUCTION, terser({ keep_fnames: true })))
        .pipe(js_filter.restore)
        .pipe(sourcemaps.write())
        .pipe(dest(paths.js_output))
}

// Vendor Javascript (always minified)
function vendorJs() {
    return src(paths.vendor_js_source)
        .pipe(errorHandler(catchError))
        .pipe(concat('vendors.js'))
        .pipe(dest(paths.js_output))
        .pipe(terser())
        .pipe(dest(paths.js_output))
}

// Image compression
function img() {
    return src(`${paths.images_source}/**/*`)
        .pipe(gulpif(PRODUCTION, imagemin())) // Compresses PNG, JPEG, GIF and SVG images
        .pipe(dest(paths.images_output))
}

// SVGs
function svg() {
    return src(`${paths.svg_source}/**/*`)
        .pipe(dest(paths.svg_output))
}

// Watch
function watchPaths() {
    // watch(`${paths.sass}/*.scss`, scss)
    watch([`${paths.js_source}/**/*.js`, `!${paths.js_source}/*.min.js`], js)
    watch([`${paths.css_source}/**/*.css`], css)
    watch([`${paths.scss_source}/**/*.scss`], scss)
    watch([`${paths.images_source}/**/*`], img)
}

// Generate all assets
const generateAssets = parallel(
    css,
    scss,
    js,
    vendorJs,
    img,
    svg
)

// Set up dev environment
const dev = parallel(
    watchPaths
)
exports["generate-assets"] = generateAssets
exports["dev"] = dev
// TODO: Look at cleaning build folder
exports.default = series(generateAssets, dev)
