import geometry;
import pathtracing;
usepackage("amsmath");
usepackage("bm");
usepackage("array");
texpreamble("\input{../../tex/macros}");
size(13cm);

pair eye = (0, 0.25);
pair x1 = (1, -0.5);

pair[] p = {
    x1,
    (3, 0.5),
    (5, -0.5),
};

pair wo = unit(x1 - eye);
drawEye(eye, wo, scale=0.5);

draw(eye--x1);
draw(x1--p[1]+0.2W--p[2]+0.5W--p[2]+0.5E--p[1]+0.2E--cycle);
draw(p[1]+0.2W--p[1]+0.2E,linewidth(2));
label("$a(\x_1 \x_2)$", p[1], N);
draw(p[2]+0.5W--p[2]+0.5E, linewidth(2));
label("$a(\x_1 \x_2 \x_3)$", p[2], S);

dot(eye--x1);
label("$\x_0$", eye, E);
label("$\x_1$", x1, S);

// draw((0.2, -0.5)--(1.8, -0.5));
// draw((2.5, 0.5)--(4.0, 0.5));