import geometry;
import pathtracing;
usepackage("amsmath");
usepackage("bm");
usepackage("array");
texpreamble("\input{../../tex/macros}");
size(10cm);

pair sun = (2.5, -0.4);

pair[] p = {
    (1, -0.5),
    (3, 0.5),
    (5, -0.25)
};
p.cyclic = true;

pair wo = 0.2unit((-1, 1));

drawSun(sun, scale=0.2, rays=16, r3=0.08);
draw(p, Arrow);

draw(p[0]--p[0]+0.5N, dashed);
markangle("${\theta_i}_0$", p[1], p[0], p[0]+N);
draw(p[1]--p[1]+0.5S, dashed);
markangle("${\theta_i}_1$", p[1]+S, p[1], p[2]);

label("$L_o(\vec{x}_0, \wo_0)$", p[0], 1.5S);

draw(p[0]--p[0]+wo, linewidth(1.5), Arrow);

for (int i = 0; i < p.length; ++i) draw(p[i]--sun+0.1unit(p[i] - sun), dashed);

dot(p[:2]);
label("$\vec{x}_0$", p[0], 2.5W);
label("$\vec{x}_1$", p[1], 2NW);
label("$\vec{x}_2$", p[2], 2SW);