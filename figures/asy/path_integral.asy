import geometry;
import pathtracing;
texpreamble("\usepackage{amsmath}\usepackage{bm}\usepackage{array}\input{../../tex/macros}");
size(12cm);

pair eye = (0, 0.25);
pair sun = (5, -0.25);

pair[] p = {
    sun,
    (3, 0.5),
    (1, -0.5),
};
p.cyclic = true;

p[0] += 0.4 * unit(p[1] - p[0]);
pair wo = unit(p[-1] - eye);
p.push(p[-1] - 0.5 * wo);

draw(p, Arrow);
draw(p[-1]--eye, dashed);
drawSun(sun, rays=10, r3=0.35);
drawEye(eye, wo);
label("$L_e(\pdir{0}{1})$", p[0], SW);
label("$\G{0}{1}$", 0.5 * (p[0] + p[1]), NE);
label("$\f{0}{1}{}$", p[1], N);
label("$\G{1}{}$", 0.5 * (p[1] + p[2]), NW);
label("$f(\pdir{1}{}, \vec{\omega_o})$", p[2], S);