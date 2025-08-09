import geometry;
import settings;
import texcolors;
outformat="pdf";
usepackage("bm");
size(6cm);

// incident and outgoing
pair wi = dir(140)*5;
//pair wo = dir(-30);
pair wm = dir(90)*5;
pair wo = reflect((0,0),(wm))*wi;

// draw wi
draw((0,0)--wi, cmyk(green), Arrow);
label("$\bm{\omega}_i$", wi, W);
markangle("$\theta_i$", wm, (0,0), wi, radius=8);

// draw wo
draw((0,0)--wo, cmyk(red), Arrow);
label("$\bm{\omega}_o$", wo, E);
markangle("$\theta_o$", wo, (0,0), wm, radius=8);

// draw wm
draw((0,0)--(wm), Arrow);
label("$\bm{\omega}_m$", wm, NW);
pair tangent = rotate(90)*wm;
draw((-tangent)--(tangent), dashed);