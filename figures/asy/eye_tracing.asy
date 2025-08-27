import geometry;
import pathtracing;
usepackage("amsmath");
usepackage("bm");
usepackage("array");
texpreamble("\input{../../tex/macros}");
size(10cm);

pair sun = (5, -0.25);

pair[] p = {
    (1, -0.5),
    (3, 0.5),
    sun,
};
p.cyclic = true;
p[-1] += 0.3 * unit(p[-2] - p[-1]);

pair wo = 0.2unit((-1, 1));

drawSun(sun, scale=0.5, rays=16, r3=0.2);
draw(p, Arrow);

draw(p[0]--p[0]+0.5N, dashed);
markangle("${\theta_i}_0$", p[1], p[0], p[0]+N);
draw(p[1]--p[1]+0.5S, dashed);
markangle("${\theta_i}_1$", p[1]+S, p[1], p[2]);

label("$L_o(\vec{x}_0, \wo_0)$", p[0], S);

draw(p[0]--p[0]+wo, linewidth(1.5), Arrow);

dot(p[:2]);
label("$\vec{x}_0$", p[0], 2.5E);
label("$\vec{x}_1$", p[1], 2NW);
label("$\vec{x}_2$", p[2], 2SW);