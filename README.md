# build-responsively
An experimental approach to responsive design.

## Idea
Pages are composed of widgets, which may be composed of other widgets
themselves. Base widgets have no children, and are created normally with HTML.
You then create a file specifying your intermediate widgets and pages. The
system then generates HTML for your pages automatically and generates CSS to
make your UI responsive.

## How to Use
1. Create an HTML file for each base widget. These go in the `src` folder.
2. Create a `app-name.json` file in the base directory specifying how widgets
   are combined (see examples).
3. Run the build script from the base directory. HTML and CSS files for each
   page are created and placed in the `build` folder.
