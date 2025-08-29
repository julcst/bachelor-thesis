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

pair[] p = {
    sun,
    (3, 0.5),
    (1, -0.5),
    (0, 0.25),
};
p.cyclic = true;
p.push(p[-1]+0.2dir(-160));

for (int i = 1; i < p.length - 1; ++i) {
    pair query = p[i];
    pair wo = unit(p[i+1] - p[i]);

    draw(p, invisible(), Arrow); // Adjust bounding box

    draw(sun-0.1sunT -- sun+0.1sunT, linewidth(1.5));
    draw(p[:i], Arrow);

    dot(query);
    label(format("$\vec{q}_%i$", i), query, 1.5S);
    //label("$L_o(\vec{x}_q, \wo_q)$", query, 1.5N);
    //label("$\x_q$", query, 1.5S);

    draw(query--query+0.2wo, linewidth(1.5), Arrow);

    for (int j = 0; j < i; ++j) {
        pair x = p[j];
        dot(x);
        label(format("$\x_%i$", j), x, 1.5S);
        draw(x--query, dashed);
    }

    shipout(format("light_bootstrapping_%i", i));
    erase();
}