#include<stdio.h>
#include<stdlib.h>

//asc2vtk.out [map.asc] [hight] [x koef] [y koef] [z koef]

int main(int argc, char **argv)
{
	if (argc != 6) goto error;

	if ((float) atoi(argv[3]) != atof(argv[3])) goto error;
	if ((float) atoi(argv[4]) != atof(argv[4])) goto error;
	if ((float) atoi(argv[5]) != atof(argv[5])) goto error;

	FILE *f = fopen(argv[1],"r");
	if (f == NULL) {
		printf("No such file\n");
		goto error;
	}

	FILE *f1 = fopen("map.txt", "w");
	int i;
	while ((i = getc(f)) != EOF) {
		if (i == ',') i = '.';
		putc(i, f1);
	}
	fclose(f1);
	fclose(f);

	f = fopen("map.txt", "r");
	int err;
	char str[20];

	float hight = atof(argv[2]);
	
	int ncols;
	if ((err = fscanf(f, "%s %d", str, &ncols)) == EOF) goto error;
	if (strcmp(str, "ncols") != 0) goto error;

	int nrows;
	if ((err = fscanf(f, "%s %d", str, &nrows)) == EOF) goto error;
	if (strcmp(str, "nrows") != 0) goto error;

	float xllcorner;
	if ((err = fscanf(f, "%s %f", str, &xllcorner)) == EOF) goto error;
	if (strcmp(str, "xllcorner") != 0) goto error;
	
	float yllcorner;
	if ((err = fscanf(f, "%s %f", str, &yllcorner)) == EOF) goto error;
	if (strcmp(str, "yllcorner") != 0) goto error;
	
	float cellsize;
	if ((err = fscanf(f, "%s %f", str, &cellsize)) == EOF) goto error;
	if (strcmp(str, "cellsize") != 0) goto error;

	float nodata_value;
	if ((err = fscanf(f, "%s %f", str, &nodata_value)) == EOF) goto error;
	if (strcmp(str, "NODATA_value") != 0) goto error;

	float *mass;
	if ((mass = (float *) malloc(ncols * nrows * sizeof(float))) == NULL) {
		printf("Memory error\n");
		goto error;
	}
	int *ind;
	if ((ind = (int *) malloc(ncols * nrows * sizeof(int))) == NULL) {
		printf("Memory error\n");
		goto error;
	}
	int *bl_cond;
	if ((bl_cond = (int *) malloc((ncols - 1) * (nrows - 1) * sizeof(int))) == NULL) {
		printf("Memory error\n");
		goto error;
	}
	int j, n_points = 0, n_cells = 0;
	for (i = 0; i < ncols * nrows; i++) {
		if (err = fscanf(f, "%f", &mass[i]) == EOF)
			goto error;
		ind[i] = -1;
		if (i < (ncols - 1) * (nrows - 1))
			bl_cond[i] = -1;
	}
	fclose(f);

	f = fopen("map.vtk", "w");
	fprintf(f, "# vtk DataFile Version 2.0\n");
	fprintf(f, "slope\n");
	fprintf(f, "ASCII\n");
	fprintf(f, "DATASET UNSTRUCTURED_GRID\n");
	for (i = 0; i < nrows; i++) {
		for (j = 0; j < ncols; j++) {
			if ((i - 1 >= 0) && (j + 1 < ncols) &&
				(mass[i * ncols + j] != nodata_value) &&
				(mass[(i - 1) * ncols + j] != nodata_value) &&
				(mass[i * ncols + j + 1] != nodata_value) &&
				(mass[(i - 1) * ncols + j + 1] != nodata_value)) {
					ind[i * ncols +j] = n_points;
					n_points++;
					goto end_points;
			}
			if ((j + 1 < ncols) && (i + 1 < nrows) &&
				(mass[i * ncols + j] != nodata_value) &&
				(mass[i * ncols + j + 1] != nodata_value) &&
				(mass[(i + 1) * ncols + j] != nodata_value) &&
				(mass[(i + 1) * ncols + j + 1] != nodata_value)) {
					ind[i * ncols + j] = n_points;
					n_points++;
					goto end_points;
			}
			if ((i + 1 < nrows) && (j - 1 >= 0) &&
				(mass[i * ncols + j] != nodata_value) &&
				(mass[(i + 1) * ncols + j] != nodata_value) &&
				(mass[i * ncols + j - 1] != nodata_value) &&
				(mass[(i + 1) * ncols + j - 1] != nodata_value)) {
					ind[i * ncols + j] = n_points;
					n_points++;
					goto end_points;
			}
			if ((j - 1 >= 0) && (i - 1 >= 0) &&
				(mass[i * ncols + j] != nodata_value) &&
				(mass[i * ncols + j - 1] != nodata_value) &&
				(mass[(i - 1) * ncols + j] != nodata_value) &&
				(mass[(i - 1) * ncols + j - 1] != nodata_value)) {
					ind[i * ncols + j] = n_points;
					n_points++;
					goto end_points;
			}
			end_points:
			if ((j - 1 >= 0) && (i - 1 >= 0) &&
				(ind[i * ncols + j] != -1) &&
				(ind[i * ncols + j - 1] != -1) &&
				(ind[(i - 1) * ncols + j - 1] != -1) &&
				(ind[(i - 1) * ncols + j] != -1)) {
					bl_cond[(i - 1) * (ncols - 1) + j - 1] = 1;
					n_cells++;
			}
		}
	}
	fprintf(f, "POINTS %d float\n", n_points * ((int) (hight / cellsize) + 1));
	int k, l, m, n, o, p, q, a;
	float interpolation, interpolation_poli;
	for (k = 0; k <= hight / cellsize * atoi(argv[5]); k++) {
		for (i = 0; i < nrows; i++) {
			for (q = 0; q < atoi(argv[4]); q++) {
				for (j = 0; j < ncols; j++) {
					for (l = 0; l < atoi(argv[3]); l++) {
						if (ind[i * ncols + j] != -1) {
							if ((q == 0) && (l == 0)) {
								fprintf(f, "%f %f %f\n", i * cellsize, j * cellsize, mass[i * ncols + j] + k * cellsize / atof(argv[5]));
							} else {
								if (((j - 1 < 0) || (ind[i * ncols + j - 1] == -1)) && (l != 0)) goto next;
								if (((i - 1 < 0) || (ind[(i - 1) * ncols + j] == -1)) && (q != 0)) goto next;
								interpolation = 0;
								for (n = 0; n < nrows; n++) {
									for (m = 0; m < ncols; m++) {
										interpolation_poli = mass[n * ncols + m];
										for (o = 0; o < nrows; o++) {
											for (p = 0; p < ncols; p++) {
												if (o != n) {
													interpolation_poli *= ((i - 1) + q / atof(argv[4]) - o) / (n - o);
												}
												if (p != m) {
													interpolation_poli *= ((j - 1) + l / atof(argv[3]) - p) / (m - p);
												}
											}
										}
										interpolation += interpolation_poli;
									}
								}
								fprintf(f, "%f %f %f\n", i * cellsize, (j - 1) * cellsize + l * cellsize / atof(argv[3]),
									mass[i * ncols + j] + k * cellsize / atof(argv[5]));
next:
								a = 0;
							}
						}
					}
				}
			}
		}
	}
	//this algorithm use n^3 operations!!!
	fprintf(f, "CELLS %d %d\n", n_cells * (int) (hight / cellsize) * 5, n_cells * (int) (hight / cellsize) * 5 * 5);
	for (k = 0; k < (hight / cellsize); k++) {
		for (i = 0; i < nrows; i++) {
			for (j = 0; j < ncols; j++) {
				if ((i - 1 >= 0) && (j - 1 >= 0) && (bl_cond[(i - 1) * (ncols - 1) + j - 1] == 1)) {
					fprintf(f, "%d %d %d %d %d\n", 4, k * n_points + ind[(i - 1) * ncols + j - 1], k * n_points + ind[(i - 1) * ncols + j],
						k * n_points + ind[i * ncols + j - 1], (k + 1) * n_points + ind[(i - 1) * ncols + j - 1]);
					fprintf(f, "%d %d %d %d %d\n", 4, k * n_points + ind[i * ncols + j - 1], k * n_points + ind[(i - 1) * ncols + j],
						k * n_points + ind[i * ncols + j], (k + 1) * n_points + ind[i * ncols + j]);
					fprintf(f, "%d %d %d %d %d\n", 4, k * n_points + ind[i * ncols + j - 1], (k + 1) * n_points + ind[(i - 1) * ncols + j - 1],
						(k + 1) * n_points + ind[i * ncols + j - 1], (k + 1) * n_points + ind[i * ncols + j]);
					fprintf(f, "%d %d %d %d %d\n", 4, k * n_points + ind[(i - 1) * ncols + j], (k + 1) * n_points + ind[(i - 1) * ncols + j - 1],
						(k + 1) * n_points + ind[(i - 1) * ncols + j], (k + 1) * n_points + ind[i * ncols + j]);
					fprintf(f, "%d %d %d %d %d\n", 4, k * n_points + ind[(i - 1) * ncols + j], k * n_points + ind[i * ncols + j - 1],
						(k + 1) * n_points + ind[(i - 1) * ncols + j - 1], (k + 1) * n_points + ind[i * ncols + j]);
				}
			}
		}
	}
	fprintf(f, "CELL_TYPES %d\n", n_cells * (int) (hight / cellsize) * 5);
	for (i = 0; i < n_cells * (int) (hight / cellsize) * 5; i++) {
		fprintf(f, "%d\n", 10);
	}

	free(mass);
	free(ind);
	free(bl_cond);
	return 0;
error:
	printf("Error\n");
	printf("asc2vtk.out [map.asc] [hight] [x koef] [y koef] [z koef]\n");
	return 1;
}
