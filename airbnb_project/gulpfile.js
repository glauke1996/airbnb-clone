const gulp = require("gulp");

const css = () => {
    const postCSS = require("gulp-postcss");
    const sass = require("gulp-sass");
    const minify = require("gulp-csso");
    sass.compiler = require("node-sass");
    return gulp
        .src("assets/scss/styles.scss")
        .pipe(sass().on("error", sass.logError))                                // sass-> css
        .pipe(postCSS([require("tailwindcss"), require("autoprefixer")]))       // tailwind -> turn them into real css 
        .pipe(minify())
        .pipe(gulp.dest("static/css"));                                         // save
};

exports.default = css;