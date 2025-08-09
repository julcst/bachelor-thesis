pair refract(pair wi, pair n, real eta=1.5) {
  real cos_theta_i = dot(wi, n);
  real sin2_theta_i = max(0, 1 - cos_theta_i^2);
  real sin2_theta_o = eta^2 * sin2_theta_i;
  // Check for total internal reflection
  if (sin2_theta_o > 1)
    return (0,0); // indicate TIR (no refraction)
  real cos_theta_o = sqrt(1 - sin2_theta_o);
  return -eta * wi + (eta * cos_theta_i - cos_theta_o) * n;
}

void drawEye(pair pos, pair dir, real scale = 1, real r1 = 0.5 * scale, real r2 = 0.6 * scale, real angle = 20, real iris = 12) {
    pair c = pos - dir * r2;
    transform t = rotate(degrees(dir), c);
    draw(t*(c+r2*dir(-angle)--c--c+r2*dir(angle)));
    draw(t*(arc(c, r1, -angle, angle)));
    path p = arc(c, r1, -iris, iris);
    pair a = point(p, 0);
    pair b = point(p, length(p));
    fill(t*((p&arc(0.5*(a+b), b, a))--cycle));
}

void drawSun(pair pos, int rays = 8, real scale = 1, real r1 = 0.2 * scale, real r2 = 0.3 * scale, real r3 = 0.5 * scale) {
    pair c = pos;
    draw(circle(c, r1));
    for (int i = 0; i < rays; ++i) {
        pair d = dir(360 / rays * i);
        draw(c + r2 * d -- c + r3 * d);
    }
}

pair[] operator --(pair[] p1, pair[] p2) {
    pair[] result;
    result.cyclic = true;
    for (int i = 0; i < p1.length; ++i) {
        result.push(p1[i]);
    }
    for (int i = 0; i < p2.length; ++i) {
        result.push(p2[i]);
    }
    return result;
}

path operator --(path p1, pair[] p2) {
    path result = p1;
    for (int i = 0; i < p2.length; ++i) {
        result = result -- p2[i];
    }
    return result;
}

path path(pair[] p) {
    path result = p[0];
    for (int i = 1; i < p.length; ++i) {
        result = result -- p[i];
    }
    return result;
}

path operator cast(pair[] p) {
    return path(p);
}

struct scene {
    path[] objects;
    
    void add(path p) {
        objects.push(p);
    }

    void draw() {
        for (int i = 0; i < objects.length; ++i) {
            draw(objects[i], gray + linewidth(1));
        }
    }

    pair[] trace(pair pos, pair dir, real start = 0, real end = 1, int length = 10) {
        pos += unit(dir) * start;
        pair[] lp = {pos};
        lp.cyclic = true;

        for (int i = 0; i < length; ++i) {
            pair hit;
            real dist = 10000;
            pair tangent;

            for (int j = 0; j < objects.length; ++j) {
                path p = objects[j];
                real[] ts = intersections(p, pos, pos + dir);
                for (int k = 0; k < ts.length; ++k) {
                    pair candidate = point(p, ts[k]);
                    real currentDist = dot(candidate - pos, dir);
                    if (currentDist < dist && currentDist > 0.1 && currentDist > 0) {
                        dist = currentDist;
                        hit = candidate;
                        tangent = dir(p, ts[k]);
                    }
                }
            }

            if (dist == 10000) {
                // No valid intersection found
                break;
            }

            pair normal = rotate(90)*tangent;
            lp.push(hit);
            pos = hit;
            dir = reflect((0,0), normal)*(-dir);
        }
        if (end > 0) lp.push(pos + unit(dir) * end);
        return lp;
    }
}