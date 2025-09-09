import geometry;
import pathtracing;
usepackage("amsmath");
usepackage("bm");
usepackage("array");
texpreamble("\input{../../tex/macros}");
size(10cm);

pair eye = (0, 0.25);
pair sun = (2.5, -0.4);

pair[] p = {
    eye,
    (1, -0.5),
    (3, 0.5),
    (5, -0.25)
};
p.cyclic = true;

pair wo = unit(p[1] - p[0]);

drawEye(eye, wo, scale=0.5);
drawSun(sun, scale=0.2, rays=16, r3=0.08);
draw(p, Arrow);

draw(p[1]--p[1]+0.5N, dashed);
markangle("${\theta}_{1\veryshortarrow2}$", p[2], p[1], p[1]+N);
draw(p[2]--p[2]+0.5S, dashed);
markangle("${\theta}_{2\veryshortarrow3}$", p[2]+S, p[2], p[3]);

for (int i = 1; i < p.length; ++i) draw(p[i]--sun+0.1unit(p[i] - sun), dashed);

dot(p[:2]);
label("$\vec{x}_0$", p[0], 2E);
label("$\vec{x}_1$", p[1], 2.5W);
label("$\vec{x}_2$", p[2], 2NW);
label("$\vec{x}_3$", p[3], 2SW);