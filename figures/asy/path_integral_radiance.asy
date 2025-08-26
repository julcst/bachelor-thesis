import geometry;
import pathtracing;
usepackage("amsmath");
usepackage("bm");
usepackage("array");
usepackage("cancel");
texpreamble("\input{../../tex/macros}");
size(13cm);

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
p.push(p[-1] - 0.3 * wo);

draw(path(p[:3]));
dot(path(p[:2]));
draw(p[-1]--eye, dashed);
drawSun(sun, scale=0.5, rays=10, r3=0.2);
drawEye(eye, wo, scale=0.5);
label("$L_e(\pdir{0}{1})$", p[0], SW);
label("$\G{0}{1}$", 0.5 * (p[0] + p[1]), NE);
label("$\f{0}{1}{2}$", p[1], N);
label("$\G{1}{2}$", 0.5 * (p[1] + p[2]), SE);
label("$\f{1}{2}{3}$", p[2], S);
label("$\cancel{\G{2}{3}}$", 0.5 * (p[2] + eye), SW);

label("$\vec{x}_0$", p[0], N);
label("$\vec{x}_1$", p[1], 1.5S);

dot(p[2]--eye, cmyk(red));
draw(p[2:4], linewidth(1.5)+cmyk(red), Arrow);
label("$\bm{\vec{x}_2}$", p[2], 2N, cmyk(red));
label("$\bm{\vec{x}_3}$", eye, 1.8S, cmyk(red));