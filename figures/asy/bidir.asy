import geometry;
import pathtracing;
usepackage("amsmath");
usepackage("bm");
usepackage("array");
texpreamble("\input{../../tex/macros}");
size(10cm);

pair sun = (5, -0.25);
pair sunN = unit(NW);
pair sunT = rotate(90)*sunN;
pair query = (0, 0.25);
pair wo = 0.2dir(-160);

pair[] p = {
    sun,
    (3, 0.5),
    (1, -0.5),
};
p.cyclic = true;

draw(sun-0.1sunT -- sun+0.1sunT, linewidth(1.5));

draw(p, Arrow);

draw(p[0]--p[0]+0.5sunN, dashed);
markangle("$\theta_{0 \veryshortarrow 1}$", p[0]+sunN, p[0], p[1]);
draw(p[1]--p[1]+0.5S, dashed);
markangle("$\theta_{1 \veryshortarrow 2}$", p[2], p[1], p[1]+S);

label("$L_o(\vec{x}_q, \wo_q)$", query, N);
dot(query);
label("$\x_q$", query, 1.5S);
draw(query--query+wo, linewidth(1.5), Arrow);

for (pair x : p) {
    draw(x--query, dashed);
}

dot(p[:2]);
label("$\vec{x}_0$", p[0], SE);
label("$\vec{x}_1$", p[1], N);
label("$\vec{x}_2$", p[2], SW);