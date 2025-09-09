import geometry;
import pathtracing;
usepackage("amsmath");
usepackage("bm");
usepackage("array");
texpreamble("\input{../../tex/macros}");
size(13cm);

void drawLo(pair x1, pair x2) {
    draw(x2--x2-0.1unit(x2-x1), linewidth(2), Arrow);
}

void drawAll(bool training = true, bool inference = true, bool reverse = false) {
    pair eye = (0, 0.25);
    pair sun = (5, -0.25);
    pair wo = unit((1.2, -0.5) - eye);

    drawSun(sun, scale=0.5, rays=16, r3=0.2);
    drawEye(eye, wo, scale=0.5);

    draw((0.2, -0.5)--(1.8, -0.5));
    draw((2.5, 0.5)--(4.0, 0.5));

    if (reverse) {
        pair[] p1 = {
            sun,
            (2.8, 0.5),
            (0.9, -0.5),
            eye
        };
        p1.cyclic = true;
        p1[0] += 0.4 * unit(p1[1] - p1[0]);
        p1[-1] -= 0.6 * unit(p1[-1] - p1[-2]);

        pair[] p2 = {
            sun,
            (3.7, 0.5),
            (1.4, -0.5),
            eye + 1E
        };
        p2.cyclic = true;
        p2[0] += 0.4 * unit(p2[1] - p2[0]);

        draw(p1, toggle(training, dotted), Arrow);
        for (int i = 1; i < p1.length - 1; ++i) drawLo(p1[i+1], p1[i]);

        draw(p2, toggle(training, dotted), Arrow);
        for (int i = 1; i < p2.length - 1; ++i) drawLo(p2[i+1], p2[i]);
    } else {
        pair[] p1 = {
            eye,
            (1, -0.5),
            (3, 0.5),
            sun
        };
        p1.cyclic = true;
        p1[-1] -= 0.3 * unit(p1[-1] - p1[-2]);

        pair[] p2 = {
            eye,
            (1.4, -0.5),
            (3.6, 0.5),
            (5, 0.25)
        };
        p2.cyclic = true;

        draw(p1, toggle(training, dotted), Arrow);
        for (int i = 1; i < p1.length - 1; ++i) drawLo(p1[i-1], p1[i]);

        draw(p2, toggle(training, dotted), Arrow);
        for (int i = 1; i < p2.length - 1; ++i) drawLo(p2[i-1], p2[i]);
    }

    draw(eye--(1.2, -0.5), toggle(inference), Arrow);
    draw(eye--(0.7, -0.5), toggle(inference), Arrow);

    draw(ellipse((1.2, -0.5), 0.3, 0.2), toggle(inference, Dotted));
    draw(ellipse((0.7, -0.5), 0.3, 0.2), toggle(inference, Dotted));
}

drawAll(training=true, inference=false);
shipout("nrc_training");
erase();
drawAll(training=false, inference=false);
shipout("nrc_cache");
erase();
drawAll(training=false, inference=true);
shipout("nrc_inference");
erase();
drawAll(reverse=true);
shipout("nrc_binrc");
erase();
drawAll(training=true, inference=true);