import geometry;
import pathtracing;
usepackage("amsmath");
usepackage("bm");
usepackage("array");
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
//p.push(p[-1] - 1.2 * wo);

draw(p, Arrow);
draw(eye--p[-1], Arrow);
drawSun(sun, scale=0.5, rays=16, r3=0.2);
drawEye(eye, wo, scale=0.5);

dot(p);
dot(eye);
label("$\vec{x}_0$", p[0], N);
label("$\vec{x}_1$", p[1], 1.5S);
label("$\vec{x}_2$", p[2], 2N);
label("$\vec{x}_3$", eye, 1.8S);