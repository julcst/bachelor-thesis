import geometry;
import pathtracing;
usepackage("amsmath");
usepackage("bm");
usepackage("array");
texpreamble("\input{../../tex/macros}");
size(12cm);

pair eye = (0, 0.25);
pair sun = (5, -0.25);

pair[] p = {
    sun,
    (3, 0.5),
    (1, -0.5),
};
p.cyclic = true;

p[0] += 0.3 * unit(p[1] - p[0]);
pair wo = unit(p[-1] - eye);
p.push(p[-1] - 1.2 * wo);

draw(p, Arrow);
//draw(p[-1]--eye, dashed);
drawSun(sun, scale=0.5, rays=10, r3=0.2);
drawEye(eye, wo, scale=0.5);
label("$L_e(\pdir{0}{1})$", p[0], SW);
label("$\G{0}{1}$", 0.5 * (p[0] + p[1]), NE);
label("$\f{0}{1}{2}$", p[1], N);
label("$\G{1}{2}$", 0.5 * (p[1] + p[2]), SE);
label("$\f{1}{2}{3}$", p[2], S);
label("$\G{2}{3}$", 0.5 * (p[2] + p[3]), SW);
label("W($\pdir{2}{3}$)", p[3], NE);