#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>

/*asc2dicts [map ascii] [snow depth] [region map ascii] [divided times x] [divided times y ] [divided times z] [hight]*/

int main(int argc, char **argv)
{
	if (argc != 8) {
		printf("Error arguments\n");
		goto exit_without_massives;
	}

	FILE *f = fopen(argv[1],"r");
	if (f == NULL) {
		printf("No such file\n");
		goto exit_without_massives;
	}

	FILE *f1 = fopen("map.txt", "w");
	int i;
	while ((i = getc(f)) != EOF) {
		if (i == ',') i = '.';
		putc(i, f1);
	}
	fclose(f1);
	fclose(f);

	f = fopen(argv[3],"r");
	if (f == NULL) {
		printf("No such file\n");
		goto exit_without_massives;
	}

	f1 = fopen("regions_map.txt", "w");
	while ((i = getc(f)) != EOF) {
		if (i == ',') i = '.';
		putc(i, f1);
	}
	fclose(f1);
	fclose(f);

	f = fopen("map.txt", "r");
	f1 = fopen("regions_map.txt", "r");

	int err;
	char str[20];

	int ncols;
	if ((err = fscanf(f, "%s %d", str, &ncols)) == EOF) goto err_file;
	if (strcmp(str, "ncols") != 0) goto err_file;

	int nrows;
	if ((err = fscanf(f, "%s %d", str, &nrows)) == EOF) goto err_file;
	if (strcmp(str, "nrows") != 0) goto err_file;

	float xllcorner;
	if ((err = fscanf(f, "%s %f", str, &xllcorner)) == EOF) goto err_file;
	if (strcmp(str, "xllcorner") != 0) goto err_file;
	
	float yllcorner;
	if ((err = fscanf(f, "%s %f", str, &yllcorner)) == EOF) goto err_file;
	if (strcmp(str, "yllcorner") != 0) goto err_file;
	
	float cellsize;
	if ((err = fscanf(f, "%s %f", str, &cellsize)) == EOF) goto err_file;
	if (strcmp(str, "cellsize") != 0) goto err_file;

	float nodata_value;
	if ((err = fscanf(f, "%s %f", str, &nodata_value)) == EOF) goto err_file;
	if (strcmp(str, "NODATA_value") != 0) goto err_file;

//	int ncols1;
//	if ((err = fscanf(f1, "%s %d", str, &ncols1)) == EOF) goto err_file;
//	if (strcmp(str, "ncols") != 0) goto err_file;
//
//	int nrows1;
//	if ((err = fscanf(f1, "%s %d", str, &nrows1)) == EOF) goto err_file;
//	if (strcmp(str, "nrows") != 0) goto err_file;
//
//	float xllcorner1;
//	if ((err = fscanf(f1, "%s %f", str, &xllcorner1)) == EOF) goto err_file;
//	if (strcmp(str, "xllcorner") != 0) goto err_file;
//	
//	float yllcorner1;
//	if ((err = fscanf(f1, "%s %f", str, &yllcorner1)) == EOF) goto err_file;
//	if (strcmp(str, "yllcorner") != 0) goto err_file;
//	
//	float cellsize1;
//	if ((err = fscanf(f1, "%s %f", str, &cellsize1)) == EOF) goto err_file;
//	if (strcmp(str, "cellsize") != 0) goto err_file;
//
//	float nodata_value1;
//	if ((err = fscanf(f1, "%s %f", str, &nodata_value1)) == EOF) goto err_file;
//	if (strcmp(str, "NODATA_value") != 0) goto err_file;
//
//	if (cellsize != cellsize1) {
//		printf("Cellsize in both maps need to be the same\n");
//		goto err_file;
//	}
//
//	if ((cellsize - (int) cellsize != 0) || (cellsize1 - (int) cellsize1 != 0)) {
//		printf("In this vercion the value cellsize need to be integer\n");
//		goto err_file;
//	}
//
//	if ((((int) fabs(xllcorner - xllcorner1)) % (int) cellsize) || ((int) fabs(yllcorner - yllcorner1) % (int) cellsize) ||
//		(fabs(xllcorner - xllcorner1) - (int) fabs(xllcorner - xllcorner1) != 0) || (fabs(yllcorner - yllcorner1) - (int) fabs(yllcorner - yllcorner1) != 0)) {
//		printf("Difference between xllcorners of maps and yllcorners need to aligned to cellsize\n");
//		goto err_file;
//	}

	float *mass;
	if ((mass = (float *) malloc(ncols * nrows * sizeof(float))) == NULL) {
		printf("Memory error (mass)\n");
		goto exit;
	}
//	float *mass1;
//	if ((mass1 = (float *) malloc(ncols1 * nrows1 * sizeof(float))) == NULL) {
//		printf("Memory error (mass1)\n");
//		goto exit;
//	}
	int *ind;
	if ((ind = (int *) malloc(ncols * nrows * sizeof(int))) == NULL) {
		printf("Memory error (ind)\n");
		goto exit;
	}
//	int *bl_cond;
//	if ((bl_cond = (int *) malloc((ncols - 1) * (nrows - 1) * sizeof(int))) == NULL) {
//		printf("Memory error (bl_cond)\n");
//		goto exit;
//	}
	float hight = atof(argv[7]);
	int j, k, l;
	for (i = 0; i < ncols * nrows; i++) {
		if (err = fscanf(f, "%f", &mass[i]) == EOF)
			goto err_file;
		ind[i] = -1;
//		if (i < (ncols - 1) * (nrows - 1))
//			bl_cond[i] = -1;
	}
//	for (i = 0; i < ncols1 * nrows1; i++) {
//		if (err = fscanf(f1, "%f", &mass1[i]) == EOF)
//			goto err_file;
//	}

	fclose(f);
	fclose(f1);

	FILE *f_vertices = fopen("vertices.txt", "w");
	fprintf(f_vertices, "vertices\n(\n");
	FILE *f_blocks = fopen("blocks.txt", "w");
	fprintf(f_blocks, "blocks\n(\n");
	FILE *f_boundary_1_sides = fopen("boundary_1_sides.txt", "w");
	fprintf(f_boundary_1_sides, "boundary\n(\n\tsides\n\t{\n\t\ttype patch;\n\t\tfaces\n\t\t(\n");
	FILE *f_boundary_2_slope = fopen("boundary_2_slope.txt", "w");
	fprintf(f_boundary_2_slope, "\tslope\n\t{\n\t\ttype wall;\n\t\tfaces\n\t\t(\n");
	FILE *f_boundary_3_atmosphere = fopen("boundary_3_atmosphere.txt", "w");
	fprintf(f_boundary_3_atmosphere, "\tatmosphere\n\t{\n\t\ttype patch;\n\t\tfaces\n\t\t(\n");
	int flag_start_line = 1;

	int n_tet = 0, n_side = 0, n_atm = 0, n_slope = 0;
	k = l = 0;
	for (i = 0; i < nrows; i++) {
		for (j = 0; j < ncols; j++) {
			if ((i -1 >= 0) && (j + 1 < ncols) &&
				(mass[i * ncols + j] != nodata_value) &&
				(mass[(i - 1) * ncols + j] != nodata_value) &&
				(mass[i * ncols + j + 1] != nodata_value) &&
				(mass[(i - 1) * ncols + j + 1] != nodata_value)) {
					ind[i * ncols +j] = k;
					k = k + 2;
//					goto point_blocks;
					goto next;
			}
			if ((j + 1 < ncols) && (i + 1 < nrows) &&
				(mass[i * ncols + j] != nodata_value) &&
				(mass[i * ncols + j + 1] != nodata_value) &&
				(mass[(i + 1) * ncols + j] != nodata_value) &&
				(mass[(i + 1) * ncols + j + 1] != nodata_value)) {
					ind[i * ncols + j] = k;
					k = k + 2;
//					goto point_blocks;
					goto next;
			}
			if ((i + 1 < nrows) && (j - 1 >= 0) &&
				(mass[i * ncols + j] != nodata_value) &&
				(mass[(i + 1) * ncols + j] != nodata_value) &&
				(mass[i * ncols + j - 1] != nodata_value) &&
				(mass[(i + 1) * ncols + j - 1] != nodata_value)) {
					ind[i * ncols + j] = k;
					k = k + 2;
//					goto point_blocks;
					goto next;
			}
			if ((j - 1 >= 0) && (i - 1 >= 0) &&
				(mass[i * ncols + j] != nodata_value) &&
				(mass[i * ncols + j - 1] != nodata_value) &&
				(mass[(i - 1) * ncols + j] != nodata_value) &&
				(mass[(i - 1) * ncols + j - 1] != nodata_value)) {
					ind[i * ncols + j] = k;
					k = k + 2;
//					goto point_blocks;
					goto next;
			}
//			point_blocks:
//			if ((j - 1 >= 0) && (i - 1 >= 0) &&
//				(ind[i * ncols + j] != -1) &&
//				(ind[i * ncols + j - 1] != -1) &&
//				(ind[(i - 1) * ncols + j - 1] != -1) &&
//				(ind[(i - 1) * ncols + j] != -1)) {
//					bl_cond[(i - 1) * (ncols - 1) + j - 1] = 1;
//			}
next:
			l++;
		}
	}

	int m, n, o, p, q, a = 0, count_ind_multipl = 0;
	float interpolation, interpolation_poli;
	int *ind_multipl;
	if ((ind_multipl = (int *) malloc(ncols * atoi(argv[4]) * nrows * atoi(argv[5]) * sizeof(int))) == NULL) {
		printf("Memory error (ind_multipl)\n");
		goto error;
	}
	int *bl_cond_multipl;
	if ((bl_cond_multipl = (int *) malloc((ncols * atoi(argv[4]) - 1) * (nrows * atoi(argv[5]) - 1) * sizeof(int))) == NULL) {
		printf("Memory error (bl_cond_multipl)\n");
		goto error;
	}
	float *mass_multipl;
	if ((mass_multipl = (float *) malloc(ncols * atoi(argv[4]) * nrows * atoi(argv[5]) * sizeof(float))) == NULL) {
		printf("Memory error (mass_multipl)\n");
		goto error;
	}
	printf("Point 1 (all massives are declarated)\n");
	for (i = 0; i < nrows; i++) {
		for (k = 0; k < atoi(argv[5]); k++) { 
			for (j = 0; j < ncols; j++) {
				for (l = 0; l < atoi(argv[4]); l++) {
					mass_multipl[i * atoi(argv[5]) * ncols * atoi(argv[4]) + k * ncols * atoi(argv[4]) + j * atoi(argv[4]) + l] = nodata_value;
					ind_multipl[i * atoi(argv[5]) * ncols * atoi(argv[4]) + k * ncols * atoi(argv[4]) + j * atoi(argv[4]) + l] = -1;
					if (ind[i * ncols + j] != -1) {
						if ((k == 0) && (l == 0)) {
							mass_multipl[i * atoi(argv[5]) * ncols * atoi(argv[4]) + k * ncols * atoi(argv[4]) + j * atoi(argv[4]) + l] = mass[i * ncols + j];
							ind_multipl[i * atoi(argv[5]) * ncols * atoi(argv[4]) + k * ncols * atoi(argv[4]) + j * atoi(argv[4]) + l] = count_ind_multipl;
							count_ind_multipl++;
						} else {
							if (((k == 0) && (j + 1 < ncols) && (ind[i * ncols + j + 1] != -1)) ||
								((l == 0) && (i + 1 < nrows) && (ind[(i + 1) * ncols + j] != -1)) ||
								((i + 1 < nrows) && (j + 1 < ncols) && (ind[(i + 1) * ncols + j] != -1) &&
								 (ind[i * ncols + j + 1] != -1) && (ind[(i + 1) * ncols + j + 1] != -1))) {
									interpolation = 0;
									for (n = 0; n < nrows; n++) {
										for (m = 0; m < ncols; m++) {
											if (ind[n * ncols + m] != -1) {
												interpolation_poli = mass[n * ncols + m];
												for (o = 0; o < nrows; o++) {
													if (o != n) {
														interpolation_poli *= (i + k / atof(argv[5]) - o) / (n - o);
													}
												}
												for (p = 0; p < ncols; p ++) {
													if (p != m) {
														interpolation_poli *= (j + l / atof(argv[4]) - p) / (m - p);
													}
												}
												interpolation += interpolation_poli;
											}
										}
									}
									mass_multipl[i * atoi(argv[5]) * ncols * atoi(argv[4]) + k * ncols * atoi(argv[4]) + j * atoi(argv[4]) + l] = interpolation;
									ind_multipl[i * atoi(argv[5]) * ncols * atoi(argv[4]) + k * ncols * atoi(argv[4]) + j * atoi(argv[4]) + l] = count_ind_multipl;
									count_ind_multipl++;
							}
						}
					}
				}
			}
		}
	}

	printf("Point 2 (interpolation was done)\n");

	for (k = 0; k <= (int) (hight / cellsize) * atoi(argv[6]); k++) {
		for (i = 0; i < nrows * atoi(argv[5]); i++) {
			for (j = 0; j < ncols * atoi(argv[4]); j++) {
				if (ind_multipl[i * ncols * atoi(argv[4]) + j] != -1) {
					fprintf(f_vertices, "\t(%f\t%f\t%f\t)\t\t// %d\n",
						i * cellsize, j * cellsize, mass_multipl[i * ncols * atoi(argv[4]) + j] + k * cellsize / atof(argv[6]), k * count_ind_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j]);
				}
			}
		}
	}

	printf("Point 3 (vertices were writen to file)\n");

	int n_points_multipl = count_ind_multipl;
	for (k = 0; k < (int) (hight / cellsize) * atoi(argv[6]); k++) {
		for (i = 0; i < nrows * atoi(argv[5]); i++) {
			for (j = 0; j < ncols * atoi(argv[4]); j++) {
				if ((k == 0) && (i != 0) && (j != 0)) {
					bl_cond_multipl[(i - 1) * (ncols * atoi(argv[4]) - 1) + j - 1] = -1;
				}
				if ((j - 1 >= 0) && (i - 1 >= 0) &&
					(ind_multipl[i * ncols * atoi(argv[4]) + j] != -1) &&
					(ind_multipl[i * ncols * atoi(argv[4]) + j - 1] != -1) &&
					(ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1] != -1) &&
					(ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j] != -1)) {
						bl_cond_multipl[(i - 1) * (ncols * atoi(argv[4]) - 1) + j - 1] = 1;
						//fprintf(f_blocks, "\ttet (%d %d %d %d) (1 1 1) simpleGrading (1 1 1) // %d\n",
						//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
						//	k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
						//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
						//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
						//	n_tet);
						//fprintf(f_blocks, "\ttet (%d %d %d %d) (1 1 1) simpleGrading (1 1 1) // %d\n",
						//	k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
						//	k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],
						//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
						//	(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],
						//	n_tet + 1);
						//fprintf(f_blocks, "\ttet (%d %d %d %d) (1 1 1) simpleGrading (1 1 1) // %d\n",
						//	k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
						//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
						//	(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
						//	(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],
						//	n_tet + 2);
						//fprintf(f_blocks, "\ttet (%d %d %d %d) (1 1 1) simpleGrading (1 1 1) // %d\n",
						//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
						//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
						//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
						//	(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],
						//	n_tet + 3);
						//fprintf(f_blocks, "\ttet (%d %d %d %d) (1 1 1) simpleGrading (1 1 1) // %d\n",
						//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
						//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
						//	k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
						//	(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],
						//	n_tet + 4);
						fprintf(f_blocks, "\thex (%d %d %d %d %d %d %d %d) (1 1 1) simpleGrading (1 1 1) // %d\n",
							k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],				// 0
							k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],						// 2
							k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],						// 2
							k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],					// 1
							(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],			// 4
							(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],			// 4
							(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],			// 4
							(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],			// 4
							n_tet);
						fprintf(f_blocks, "\thex (%d %d %d %d %d %d %d %d) (1 1 1) simpleGrading (1 1 1) // %d\n",
							k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],						// 2
							k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],							// 3
							k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],							// 3
							k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],					// 1
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							n_tet + 1);
						fprintf(f_blocks, "\thex (%d %d %d %d %d %d %d %d) (1 1 1) simpleGrading (1 1 1) // %d\n",
							k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],						// 2
							(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],			// 4
							(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],			// 4
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],				// 6
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							n_tet + 2);
						fprintf(f_blocks, "\thex (%d %d %d %d %d %d %d %d) (1 1 1) simpleGrading (1 1 1) // %d\n",
							k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],					// 1
							(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],				// 5
							(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],				// 5
							(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],			// 4
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							n_tet + 3);
						fprintf(f_blocks, "\thex (%d %d %d %d %d %d %d %d) (1 1 1) simpleGrading (1 1 1) // %d\n",
							k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],					// 1
							(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],			// 4
							(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],			// 4
							k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],						// 2
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							n_tet + 4);
						n_tet += 5;
						if (k == (int) (hight / cellsize) * atoi(argv[6]) - 1) {
							//fprintf(f_boundary_3_atmosphere, "\t\t\t(%d\t%d\t%d\t)\t\t// %d\n",
							//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
							//	(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],
							//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
							//	n_atm);
							//fprintf(f_boundary_3_atmosphere, "\t\t\t(%d\t%d\t%d\t)\t\t// %d\n",
							//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
							//	(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
							//	(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],
							//	n_atm + 1);
							fprintf(f_boundary_3_atmosphere, "\t\t\t(%d\t%d\t%d\t%d)\t\t// %d\n",
								(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],		// 4
								(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],				// 7
								(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],				// 7
								(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],			// 5
								n_atm);
							fprintf(f_boundary_3_atmosphere, "\t\t\t(%d\t%d\t%d\t%d)\t\t// %d\n",
								(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],		// 4
								(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],			// 6
								(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],				// 7
								(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],				// 7
								n_atm + 1);
							n_atm += 2;
						}
						if (k == 0) {
							//fprintf(f_boundary_2_slope, "\t\t\t(%d\t%d\t%d\t)\t\t// %d\n",
							//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
							//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
							//	k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
							//	n_slope);
							//fprintf(f_boundary_2_slope, "\t\t\t(%d\t%d\t%d\t)\t\t// %d\n",
							//	k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],
							//	k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
							//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
							//	n_slope + 1);
							fprintf(f_boundary_2_slope, "\t\t\t(%d\t%d\t%d\t%d)\t\t// %d\n",
								k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],			// 0
								k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],				// 1
								k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],					// 2
								k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],					// 2
								n_slope);
							fprintf(f_boundary_2_slope, "\t\t\t(%d\t%d\t%d\t%d)\t\t// %d\n",
								k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],						// 3
								k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],						// 3
								k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],					// 2
								k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],				// 1
								n_slope + 1);
							n_slope += 2;
						}
				}
				if ((i - 1 >= 0) && (j - 1 >= 0) &&
					(((j - 2 < 0) && (bl_cond_multipl[(i - 1) * (ncols * atoi(argv[4]) - 1) + j - 1] == 1)) ||
					 ((j - 2 >= 0) && (bl_cond_multipl[(i - 1) * (ncols * atoi(argv[4]) - 1) + j - 1] *
						 bl_cond_multipl[(i - 1) * (ncols * atoi(argv[4]) - 1) + j - 2] < 0)))) {
							if (bl_cond_multipl[(i - 1) * (ncols * atoi(argv[4]) - 1) + j - 1] == 1) {
								printf("Sides must be written\n");
								//fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t)\t\t// %d\n",
								//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
								//	k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
								//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
								//	n_side);
								//fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t)\t\t// %d\n",
								//	(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
								//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
								//	k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
								//	n_side + 1);
								fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\t\t// %d\n",
									k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],		// 0
									k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],				// 2
									(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],	// 4
									(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],	// 4
									n_side);
								fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\t\t// %d\n",
									(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],		// 6
									(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],	// 4
									(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],	// 4
									k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],				// 2
									n_side + 1);
								n_side += 2;
							} else {
								printf("Sides must be written\n");
								//fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t)\t\t// %d\n",
								//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
								//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
								//	(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
								//	n_side);
								//fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t)\t\t// %d\n",
								//	(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
								//	k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
								//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
								//	n_side + 1);
								fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\t\t// %d\n",
									k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],		// 0
									(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],	// 4
									(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],		// 6
									(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],		// 6
									n_side);
								fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\t\t// %d\n",
									(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],		// 6
									(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],		// 6
									k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],				// 2
									k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],		// 0
									n_side + 1);
								n_side += 2;
							}
				}
				if ((i - 1 >= 0) && (j - 1 >= 0) &&
					(((i - 2 < 0) && (bl_cond_multipl[(i - 1) * (ncols * atoi(argv[4]) - 1) + j - 1] == 1)) ||
					 ((i - 2 >= 0) && (bl_cond_multipl[(i - 1) * (ncols * atoi(argv[4]) - 1) + j - 1] *
						 bl_cond_multipl[(i - 2) * (ncols * atoi(argv[4]) - 1) + j - 1] < 0)))) {
							if (bl_cond_multipl[(i - 1) * (ncols * atoi(argv[4]) - 1) + j - 1] == 1) {
								printf("Sides must be written\n");
								//fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t)\t\t// %d\n",
								//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
								//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
								//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
								//	n_side);
								//fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t)\t\t// %d\n",
								//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
								//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
								//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
								//	n_side + 1);
								fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\t\t// %d\n",
									k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],		// 0
									(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],	// 4
									(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],	// 4
									k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],			// 1
									n_side);
								fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\t\t// %d\n",
									(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],	// 4
									(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],		// 5
									(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],		// 5
									k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],			// 1
									n_side + 1);
								n_side += 2;
							} else {
								printf("Sides must be written\n");
								//fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t)\t\t// %d\n",
								//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
								//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
								//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
								//	n_side);
								//fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t)\t\t// %d\n",
								//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],
								//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
								//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
								//	n_side + 1);
								fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\t\t// %d\n",
									k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],		// 0
									(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],		// 5
									(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],		// 5
									(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],	// 4
									n_side);
								fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\t\t// %d\n",
									k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j - 1],		// 0
									k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],			// 1
									(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],		// 5
									(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],		// 5
									n_side + 1);
								n_side += 2;
							}
				}
				if ((i - 1 >= 0) && (j == ncols * atoi(argv[4]) - 1) &&
					(bl_cond_multipl[(i - 1) * (ncols * atoi(argv[4]) - 1) + j - 1] == 1)) {
						printf("Sides must be written\n");
						//fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t)\t\t// %d\n",
						//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
						//	(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
						//	(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],
						//	n_side);
						//fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t)\t\t// %d\n",
						//	(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],
						//	k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],
						//	k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],
						//	n_side + 1);
						fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\t\t// %d\n",
							k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],					// 1
							(k + 1) * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],				// 5
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							n_side);
						fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\t\t// %d\n",
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],							// 3
							k * n_points_multipl + ind_multipl[(i - 1) * ncols * atoi(argv[4]) + j],					// 1
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							n_side + 1);
						n_side += 2;
				}
				if ((j - 1 >= 0) && (i == nrows * atoi(argv[5]) - 1) &&
					(bl_cond_multipl[(i - 1) * (ncols * atoi(argv[4]) - 1) + j - 1] == 1)) {
						printf("Sides must be written\n");
						//fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t)\t\t// %d\n",
						//	k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
						//	k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],
						//	(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],
						//	n_side);
						//fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t)\t\t// %d\n",
						//	(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
						//	k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],
						//	(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],
						//	n_side + 1);
						fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\t\t// %d\n",
							k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],						// 2
							k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],							// 3
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							n_side);
						fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\t\t// %d\n",
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],				// 6
							k * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j - 1],						// 2
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							(k + 1) * n_points_multipl + ind_multipl[i * ncols * atoi(argv[4]) + j],					// 7
							n_side + 1);
						n_side += 2;
				}
			}
		}
	}

	printf("bl_cond_multipl massive print\n");
	for (i = 0; i < nrows * atoi(argv[5]) - 1; i++) {
		for (j = 0; j < ncols * atoi(argv[4]) - 1; j++) {
			printf("bl_cond_multipl[%d] = %d\n", i * (ncols * atoi(argv[4]) - 1) + j, bl_cond_multipl[i * (ncols * atoi(argv[4]) - 1) + j]);
		}
	}

	printf("Point 4 (blocks and boundaries were writen to file)\n");

	fprintf(f_boundary_3_atmosphere, "\t\t);\n\t}\n);\n");
	fclose(f_boundary_3_atmosphere);
	fprintf(f_boundary_2_slope, "\t\t);\n\t}\n");
	fclose(f_boundary_2_slope);
	fprintf(f_boundary_1_sides, "\t\t);\n\t}\n");
	fclose(f_boundary_1_sides);
	fprintf(f_blocks, ");\n");
	fclose(f_blocks);
	fprintf(f_vertices, ");\n");
	fclose(f_vertices);

	f_vertices = fopen("vertices.txt", "r");
	f_blocks = fopen("blocks.txt", "r");
	f_boundary_1_sides = fopen("boundary_1_sides.txt", "r");
	f_boundary_2_slope = fopen("boundary_2_slope.txt", "r");
	f_boundary_3_atmosphere = fopen("boundary_3_atmosphere.txt", "r");
	f = fopen("blockMeshDict", "w");
	fprintf(f, "FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tobject\tblockMeshDict;\n}\nconvertToMeters 1;\n");
	while ((i = getc(f_vertices)) != EOF)
		putc(i, f);
	fprintf(f, "\n");
	while ((i = getc(f_blocks)) != EOF)
		putc(i, f);
	fprintf(f, "\nedges\n(\n);\n\n");
	while ((i = getc(f_boundary_1_sides)) != EOF)
		putc(i, f);
	fprintf(f, "\n");
	while ((i = getc(f_boundary_2_slope)) != EOF)
		putc(i, f);
	while ((i = getc(f_boundary_3_atmosphere)) != EOF)
		putc(i, f);
	fprintf(f, "\nmergePatchPairs\n(\n);\n");

	fclose(f_boundary_3_atmosphere);
	fclose(f_boundary_2_slope);
	fclose(f_boundary_1_sides);
	fclose(f_blocks);
	fclose(f_vertices);
	fclose(f);

	printf("Point 5 (combining files to dict)\n");

//	int *snow_region = (int *) malloc(ncols * nrows * sizeof(int));
//	float xlucorner = xllcorner;
//	float ylucorner = yllcorner + cellsize * nrows;
//	float xlucorner1 = xllcorner1;
//	float ylucorner1 = yllcorner1 + cellsize1 * nrows1;
//	for (i = 0; i < nrows; i++) {
//		for (j = 0; j < ncols; j++) {
//			if ((xlucorner1 - xlucorner >= 0) && (ylucorner -ylucorner1 >= 0) &&
//				(j >= ((int) (xlucorner1 - xlucorner)) / cellsize) && (i >= ((int) (ylucorner - ylucorner1)) / cellsize) &&
//				(j < ((int) (xlucorner1 - xlucorner)) / cellsize + ncols1) && (i < ((int) (ylucorner - ylucorner1)) / cellsize + nrows1)) {
//					if (mass1[(i - ((int) (ylucorner - ylucorner1)) / (int) cellsize) * ncols1 + j - ((int) (xlucorner1 - xlucorner)) / (int) cellsize] == 1)
//						snow_region[i * ncols + j] = 1;
//					else if (mass1[(i - ((int) (ylucorner - ylucorner1)) / (int) cellsize) * ncols1 + j - ((int) (xlucorner1 - xlucorner)) / (int) cellsize] == 0)
//						snow_region[i * ncols + j] = 0;
//					else
//						snow_region[i * ncols + j] = -1;
//			} else {
//					snow_region[i * ncols + j] = -1;
//			}
//		}
//	}
//
//	f = fopen("alpha.water", "w");
//	f1 = fopen("region", "w");
//	fprintf(f, "FoamFile\n");
//	fprintf(f, "{\n");
//	fprintf(f, "\tversion\t2.0;\n");
//	fprintf(f, "\tformat\tascii;\n");
//	fprintf(f, "\tclass\tvolScalarField;\n");
//	fprintf(f, "\tlocation\t\"0\";\n");
//	fprintf(f, "\tobject\talpha.water;\n");
//	fprintf(f, "}\n\n");
//	fprintf(f, "dimensions\t[0 0 0 0 0 0 0];\n\n");
//	fprintf(f, "internalField\tnonuniform List<scalar>\n");
//	fprintf(f, "%d\n", n_tet);
//	fprintf(f, "(\n");
//	fprintf(f1, "FoamFile\n");
//	fprintf(f1, "{\n");
//	fprintf(f1, "\tversion\t2.0;\n");
//	fprintf(f1, "\tformat\tascii;\n");
//	fprintf(f1, "\tclass\tvolScalarField;\n");
//	fprintf(f1, "\tlocation\t\"0\";\n");
//	fprintf(f1, "\tobject\tregion;\n");
//	fprintf(f1, "}\n\n");
//	fprintf(f1, "dimensions\t[0 0 0 0 0 0 0];\n\n");
//	fprintf(f1, "internalField\tnonuniform List<scalar>\n");
//	fprintf(f1, "%d\n", n_tet);
//	fprintf(f1, "(\n");
//	float w_ind;
//	for (i = 0; i < nrows - 1; i++) {
//		for (m = 0; m < atoi(argv[5]); m++) {
//			for (j = 0; j < ncols - 1; j++) {
//				for (l = 0; l < atoi(argv[4]); l++) {
//					for (k = 0; k < atoi(argv[6]); k++) {
//						if (((k + 1) * (hight / atof(argv[6])) < atof(argv[2])) && (bl_cond[i * (ncols - 1) + j] !=  -1) && (snow_region[i * ncols + j] == 0))
//							w_ind = 1;
//						else
//							if ((k * (hight / atof(argv[6])) < atof(argv[2])) && (bl_cond[i * (ncols - 1) + j] !=  -1) && (snow_region[i * ncols + j] == 0))
//								w_ind = (atof(argv[2]) - k * (hight / atof(argv[6]))) / (hight / atof(argv[6]));
//							else
//								w_ind = 0;
//						if (bl_cond[i * (ncols - 1) + j] !=  -1) {
//							if ((w_ind == 0) || (w_ind == 1))
//								fprintf(f, "%d\n", (int) w_ind);
//							else
//								fprintf(f, "%e\n", w_ind);
//							if ((w_ind > 1) || (w_ind < 0))
//								printf("error in alpha.water file\n");
//						}
//						if ((bl_cond[i * (ncols - 1) + j] !=  -1) && (snow_region[i * ncols + j] == 1))
//							w_ind = 1;
//						else
//							w_ind = 0;
//						if (bl_cond[i * (ncols - 1) + j] !=  -1) {
//							if ((w_ind == 0) || (w_ind == 1))
//								fprintf(f1, "%d\n", (int) w_ind);
//							else
//								fprintf(f1, "%e\n", w_ind);
//							if ((w_ind > 1) || (w_ind < 0))
//								printf("error in alpha.water file\n");
//						}
//					}
//				}
//			}
//		}
//	}
//	fprintf(f, ")\n;\n\n");
//	fprintf(f, "boundaryField\n");
//	fprintf(f, "{\n");
//	fprintf(f, "\tsides\n");
//	fprintf(f, "\t{\n");
//	fprintf(f, "\t\ttype\t\tinletOutlet;\n");
//	fprintf(f, "\t\tinletValue\tuniform 0;\n");
//	fprintf(f, "\t\tvalue\t\tuniform 0;\n");
//	fprintf(f, "\t}\n");
//	fprintf(f, "\tslope\n");
//	fprintf(f, "\t{\n");
//	fprintf(f, "\t\ttype\t\tzeroGradient;\n");
//	fprintf(f, "\t}\n");
//	fprintf(f, "\tatmosphere\n");
//	fprintf(f, "\t{\n");
//	fprintf(f, "\t\ttype\t\tinletOutlet;\n");
//	fprintf(f, "\t\tinletValue\tuniform 0;\n");
//	fprintf(f, "\t\tvalue\t\tuniform 0;\n");
//	fprintf(f, "\t}\n");
//	fprintf(f, "}\n");
//	fclose(f);
//	fprintf(f1, ")\n;\n\n");
//	fprintf(f1, "boundaryField\n");
//	fprintf(f1, "{\n");
//	fprintf(f1, "\tsides\n");
//	fprintf(f1, "\t{\n");
//	fprintf(f1, "\t\ttype\t\tinletOutlet;\n");
//	fprintf(f1, "\t\tinletValue\tuniform 0;\n");
//	fprintf(f1, "\t\tvalue\t\tuniform 0;\n");
//	fprintf(f1, "\t}\n");
//	fprintf(f1, "\tslope\n");
//	fprintf(f1, "\t{\n");
//	fprintf(f1, "\t\ttype\t\tzeroGradient;\n");
//	fprintf(f1, "\t}\n");
//	fprintf(f1, "\tatmosphere\n");
//	fprintf(f1, "\t{\n");
//	fprintf(f1, "\t\ttype\t\tinletOutlet;\n");
//	fprintf(f1, "\t\tinletValue\tuniform 0;\n");
//	fprintf(f1, "\t\tvalue\t\tuniform 0;\n");
//	fprintf(f1, "\t}\n");
//	fprintf(f1, "}\n");
//	fclose(f1);

	free(mass_multipl);
	free(bl_cond_multipl);
	free(ind_multipl);
	free(ind);
//	free(mass1);
	free(mass);
//	free(bl_cond);
//	free(snow_region);

	return 0;

exit:
	free(mass);
//	free(mass1);
	free(ind);
//	free(bl_cond);
err_file:
	fclose(f);
	fclose(f1);
	printf("Error file\n");
exit_without_massives:
error:
	printf("asc2dicts [map ascii] [snow depth] [region map ascii] [divided times x] [divided times y ] [divided times z] [hight]\n");
	return 1;
}
