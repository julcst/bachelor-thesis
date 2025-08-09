import geometry;
import settings;
import fontsize;
import texcolors;
outformat="pdf";
usepackage("bm");
size(6cm);

pair refract(pair wi, pair n, real eta) {
  real cos_theta_i = dot(wi, n);
  real sin2_theta_i = max(0, 1 - cos_theta_i^2);
  real sin2_theta_o = eta^2 * sin2_theta_i;

  // Check for total internal reflection
  if (sin2_theta_o > 1)
    return (0,0); // indicate TIR (no refraction)

  real cos_theta_o = sqrt(1 - sin2_theta_o);
  return -eta * wi + (eta * cos_theta_i - cos_theta_o) * n;
}

// eta
real etai = 1.5;
real etao = 2.0;
real eta = etao / etai;

// incident and outgoing
pair wi = dir(140);
//pair wo = dir(-30);
pair wm = dir(90);
//pair wm = unit(eta * wi + wo);
pair wo = refract(wi, wm, 1 / eta);

// draw wi
draw((0,0)--wi, cmyk(green), Arrow);
label("$\bm{\omega}_i$", wi, W);
draw((0,dot(wi,wm))--wi);
label("$\sin(\theta_i)$", wi+(0.3,0), N, fontsize(4pt));
markangle("$\theta_i$", wm, (0,0), wi, radius=8);

draw((0,0)--etai*wi, cmyk(green)+dotted, Arrow);
label("$\eta_i\bm{\omega}_i$", etai*wi, W);
draw((0,dot(etai*wi,wm))--etai*wi, dotted);
label("$\eta_i\sin(\theta_i)$", etai*wi+(0.5,0), N, fontsize(4pt));

draw(etao*wo--etai*wi+etao*wo, cmyk(green)+dotted, Arrow);

// draw wo
draw((0,0)--wo, cmyk(red), Arrow);
label("$\bm{\omega}_o$", wo, E);
draw((0,dot(wo,wm))--wo);
label("$\sin(\theta_o)$", wo-(0.2,0), S, fontsize(4pt));
markangle("$\theta_o$", -wm, (0,0), wo, radius=8);

draw((0,0)--etao*wo, cmyk(red)+dotted, Arrow);
label("$\eta_o\bm{\omega}_o$", etao*wo, E);
draw((0,dot(etao*wo,wm))--etao*wo, dotted);
label("$\eta_o\sin(\theta_o)$", etao*wo-(0.5,0), S, fontsize(4pt));

draw(etai*wi--etao*wo+etai*wi, cmyk(red)+dotted, Arrow);

// draw wm
draw((0,0)--unit(etai*wi+etao*wo), Arrow);
draw((-etao*wm)--etai*wm, dashed);
label("$\bm{\omega}_m$", unit(wi*etai+wo*etao), SW);
pair tangent = rotate(90)*wm*etai;
draw((-tangent)--(tangent), dashed);