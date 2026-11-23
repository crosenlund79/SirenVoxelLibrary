/* Optional accelerated voxel DDA for voxrender.py (same algorithm as the numpy path).
 * Build: gcc -O3 -fopenmp -shared -fPIC vtrace.c -o vtrace.so   (done automatically). */
#include <math.h>
#include <stdint.h>

void vtrace(const uint16_t *grid, int nx, int ny, int nz,
            const double *o, const double *d, long n, double tmax,
            uint8_t *hit, double *tout, int8_t *axis_out, int8_t *sign_out,
            uint16_t *col_out)
{
    const long sx = (long)ny * nz, sy = nz;
    const double dims[3] = {nx, ny, nz};
    const int dimi[3] = {nx, ny, nz};
#pragma omp parallel for schedule(dynamic, 1024)
    for (long i = 0; i < n; i++) {
        double oo[3], dd[3], inv[3], tm[3], tdel[3];
        int cell[3], step[3];
        hit[i] = 0; tout[i] = INFINITY; axis_out[i] = 0; sign_out[i] = 0; col_out[i] = 0;
        double tn = -INFINITY, tf = INFINITY;
        int enter_axis = 0;
        for (int k = 0; k < 3; k++) {
            oo[k] = o[3 * i + k];
            dd[k] = d[3 * i + k];
            if (fabs(dd[k]) < 1e-12) dd[k] = 1e-12;
            inv[k] = 1.0 / dd[k];
            double t1 = -oo[k] * inv[k], t2 = (dims[k] - oo[k]) * inv[k];
            double a = t1 < t2 ? t1 : t2, b = t1 < t2 ? t2 : t1;
            if (a > tn) { tn = a; enter_axis = k; }
            if (b < tf) tf = b;
        }
        if (tmax < tf) tf = tmax;
        int inside = tn <= 0;
        if (tn < 0) tn = 0;
        if (!(tn < tf)) continue;
        double tc = tn;
        for (int k = 0; k < 3; k++) {
            double p = oo[k] + dd[k] * (tc + 1e-6);
            int c = (int)floor(p);
            if (c < 0) c = 0;
            if (c > dimi[k] - 1) c = dimi[k] - 1;
            cell[k] = c;
            step[k] = dd[k] > 0 ? 1 : -1;
            tdel[k] = fabs(inv[k]);
            double nb = step[k] > 0 ? cell[k] + 1 : cell[k];
            tm[k] = (nb - oo[k]) * inv[k];
        }
        int ax = inside ? -1 : enter_axis;
        for (;;) {
            uint16_t c = grid[cell[0] * sx + cell[1] * sy + cell[2]];
            if (c) {
                int a2 = ax < 0 ? 2 : ax;
                hit[i] = 1; tout[i] = tc; axis_out[i] = (int8_t)a2;
                sign_out[i] = (int8_t)(-step[a2]); col_out[i] = c;
                break;
            }
            int a = 0;
            if (tm[1] < tm[a]) a = 1;
            if (tm[2] < tm[a]) a = 2;
            tc = tm[a];
            cell[a] += step[a];
            tm[a] += tdel[a];
            ax = a;
            if (!(tc < tf) || cell[a] < 0 || cell[a] >= dimi[a]) break;
        }
    }
}
