import geometry;
import pathtracing;
usepackage("amsmath");
usepackage("bm");
usepackage("array");
texpreamble("\input{../../tex/macros}");
size(13cm);

pair eye = (0, 0.25);
pair query = (5, -0.25);

pair[] p = {
    eye,
    (1, -0.5),
    (3, 0.5),
    query,
};
p.cyclic = true;

pair wo = unit(p[1] - p[0]);

drawEye(eye, wo, scale=0.5);
draw(path(p));

draw(p[1]--p[1]+0.5N, dashed);
markangle("$\theta_{1\veryshortarrow2}$", p[2], p[1], p[1]+N);
draw(p[2]--p[2]+0.5S, dashed);
markangle("$\theta_{2\veryshortarrow3}$", p[2]+S, p[2], p[3]);

label("$\f{2}{1}{0}$", p[1], S);
label("$\f{3}{2}{1}$", p[2], N);
label("$\widehat{L}_o(\pdir{3}{2})$", p[3], S);

draw(p[3]--p[3] + 0.2unit(p[2] - p[3]), linewidth(1.5), Arrow);

dot(p);
label("$\vec{x}_0$", p[0], 1.5E);
label("$\vec{x}_1$", p[1], 2NW+1.5N);
label("$\vec{x}_2$", p[2], 2SW+S);
label("$\vec{x}_3$", p[3], E);