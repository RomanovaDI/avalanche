#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>

/*asc2dicts [map ascii] [divided times] [volume of avalanche] [region map ascii]*/

int main(int argc, char **argv)
{
	if (argc > 5) {
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

	f = fopen(argv[4],"r");
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

	int ncols1;
	if ((err = fscanf(f1, "%s %d", str, &ncols1)) == EOF) goto err_file;
	if (strcmp(str, "ncols") != 0) goto err_file;

	int nrows1;
	if ((err = fscanf(f1, "%s %d", str, &nrows1)) == EOF) goto err_file;
	if (strcmp(str, "nrows") != 0) goto err_file;

	float xllcorner1;
	if ((err = fscanf(f1, "%s %f", str, &xllcorner1)) == EOF) goto err_file;
	if (strcmp(str, "xllcorner") != 0) goto err_file;
	
	float yllcorner1;
	if ((err = fscanf(f1, "%s %f", str, &yllcorner1)) == EOF) goto err_file;
	if (strcmp(str, "yllcorner") != 0) goto err_file;
	
	float cellsize1;
	if ((err = fscanf(f1, "%s %f", str, &cellsize1)) == EOF) goto err_file;
	if (strcmp(str, "cellsize") != 0) goto err_file;

	float nodata_value1;
	if ((err = fscanf(f1, "%s %f", str, &nodata_value1)) == EOF) goto err_file;
	if (strcmp(str, "NODATA_value") != 0) goto err_file;

	if (cellsize != cellsize1) {
		printf("Cellsize in both maps need to be the same\n");
		goto err_file;
	}

	if ((cellsize - (int) cellsize != 0) || (cellsize1 - (int) cellsize1 != 0)) {
		printf("In this vercion the value cellsize need to be integer\n");
		goto err_file;
	}

	if ((((int) fabs(xllcorner - xllcorner1)) % (int) cellsize) || ((int) fabs(yllcorner - yllcorner1) % (int) cellsize) ||
		(fabs(xllcorner - xllcorner1) - (int) fabs(xllcorner - xllcorner1) != 0) || (fabs(yllcorner - yllcorner1) - (int) fabs(yllcorner - yllcorner1) != 0)) {
		printf("Difference between xllcorners of maps and yllcorners need to aligned to cellsize\n");
		goto err_file;
	}

	float *mass;
	if ((mass = (float *) malloc(ncols * nrows * sizeof(float))) == NULL) {
		printf("Memory error\n");
		goto exit;
	}
	float *mass1;
	if ((mass1 = (float *) malloc(ncols1 * nrows1 * sizeof(float))) == NULL) {
		printf("Memory error\n");
		goto exit;
	}
	int *ind;
	if ((ind = (int *) malloc(ncols * nrows * sizeof(int))) == NULL) {
		printf("Memory error\n");
		goto exit;
	}
	int *bl_cond;
	if ((bl_cond = (int *) malloc((ncols - 1) * (nrows - 1) * sizeof(int))) == NULL) {
		printf("Memory error\n");
		goto exit;
	}
	float hight = 20;
	int j, k;
	for (i = 0; i < ncols * nrows; i++) {
		if (err = fscanf(f, "%f", &mass[i]) == EOF)
			goto err_file;
		ind[i] = -1;
		if (i < (ncols - 1) * (nrows - 1))
			bl_cond[i] = -1;
	}
	for (i = 0; i < ncols1 * nrows1; i++) {
		if (err = fscanf(f1, "%f", &mass1[i]) == EOF)
			goto err_file;
	}

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

	int n_hex = 0, n_side = 0, n_atm = 0, n_slope = 0;
	float min_z = mass[0], max_z = mass[0];
	k = 0;
	for (i = 0; i < nrows; i++) {
		for (j = 0; j < ncols; j++) {
			if ((mass[i * ncols + j] != nodata_value) && (mass[i * ncols + j] < min_z))
				min_z = mass[i * ncols + j];
			if ((mass[i * ncols + j] != nodata_value) && (mass[i * ncols + j] > max_z))
				max_z = mass[i * ncols + j];
			if ((i -1 >= 0) && (j + 1 < ncols) &&
				(mass[i * ncols + j] != nodata_value) &&
				(mass[(i - 1) * ncols + j] != nodata_value) &&
				(mass[i * ncols + j + 1] != nodata_value) &&
				(mass[(i - 1) * ncols + j + 1] != nodata_value)) {
					ind[i * ncols +j] = k;
					fprintf(f_vertices, "\t(%f\t%f\t%f\t)\t\t// %d\n",
						i * cellsize, j * cellsize, mass[i * ncols + j], ind[i * ncols + j]);
					fprintf(f_vertices, "\t(%f\t%f\t%f\t)\t\t// %d\n",
						i * cellsize, j * cellsize, mass[i * ncols + j] + hight, ind[i * ncols + j] + 1);
					k = k + 2;
					goto point_blocks;
			}
			if ((j + 1 < ncols) && (i + 1 < nrows) &&
				(mass[i * ncols + j] != nodata_value) &&
				(mass[i * ncols + j + 1] != nodata_value) &&
				(mass[(i + 1) * ncols + j] != nodata_value) &&
				(mass[(i + 1) * ncols + j + 1] != nodata_value)) {
					ind[i * ncols + j] = k;
					fprintf(f_vertices, "\t(%f\t%f\t%f\t)\t\t// %d\n",
						i * cellsize, j * cellsize, mass[i * ncols + j], ind[i * ncols + j]);
					fprintf(f_vertices, "\t(%f\t%f\t%f\t)\t\t// %d\n",
						i * cellsize, j * cellsize, mass[i * ncols + j] + hight,ind[i * ncols + j] + 1);
					k = k + 2;
					goto point_blocks;
			}
			if ((i + 1 < nrows) && (j - 1 >= 0) &&
				(mass[i * ncols + j] != nodata_value) &&
				(mass[(i + 1) * ncols + j] != nodata_value) &&
				(mass[i * ncols + j - 1] != nodata_value) &&
				(mass[(i + 1) * ncols + j - 1] != nodata_value)) {
					ind[i * ncols + j] = k;
					fprintf(f_vertices, "\t(%f\t%f\t%f\t)\t\t// %d\n",
						i * cellsize, j * cellsize, mass[i * ncols + j], ind[i * ncols + j]);
					fprintf(f_vertices, "\t(%f\t%f\t%f\t)\t\t// %d\n",
						i * cellsize, j * cellsize, mass[i * ncols + j] + hight,ind[i * ncols + j] + 1);
					k = k + 2;
					goto point_blocks;
			}
			if ((j - 1 >= 0) && (i - 1 >= 0) &&
				(mass[i * ncols + j] != nodata_value) &&
				(mass[i * ncols + j - 1] != nodata_value) &&
				(mass[(i - 1) * ncols + j] != nodata_value) &&
				(mass[(i - 1) * ncols + j - 1] != nodata_value)) {
					ind[i * ncols + j] = k;
					fprintf(f_vertices, "\t(%f\t%f\t%f\t)\t\t// %d\n",
						i * cellsize, j * cellsize, mass[i * ncols + j], ind[i * ncols + j]);
					fprintf(f_vertices, "\t(%f\t%f\t%f\t)\t\t// %d\n",
						i * cellsize, j * cellsize, mass[i * ncols + j] + hight,ind[i * ncols + j] + 1);
					k = k + 2;
					goto point_blocks;
			}
			point_blocks:
			if ((j - 1 >= 0) && (i - 1 >= 0) &&
				(ind[i * ncols + j] != -1) &&
				(ind[i * ncols + j - 1] != -1) &&
				(ind[(i - 1) * ncols + j - 1] != -1) &&
				(ind[(i - 1) * ncols + j] != -1)) {
					bl_cond[(i - 1) * (ncols - 1) + j - 1] = 1;
					fprintf(f_blocks, "\thex (%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t)\t(%d\t%d\t%d\t)\tsimpleGrading (1 1 1)\t\t// %d\t%d\t%d\n",
						ind[(i - 1) * ncols + j - 1], ind[i * ncols + j - 1], ind[i * ncols + j], ind[(i - 1) * ncols + j],
						ind[(i - 1) * ncols + j - 1] + 1, ind[i * ncols + j - 1] + 1, ind[i * ncols + j] + 1, ind[(i - 1) * ncols + j] + 1,
						atoi(argv[2]), atoi(argv[2]), (int) (hight * atoi(argv[2]) / cellsize), n_hex, i, j);
					n_hex++;
					fprintf(f_boundary_3_atmosphere, "\t\t\t(%d\t%d\t%d\t%d\t)\t\t// %d\n",
						ind[i * ncols + j] + 1, ind[(i - 1) * ncols + j] + 1, ind[(i - 1) * ncols + j - 1] + 1, ind[i * ncols + j - 1] + 1,
						n_atm);
					n_atm++;
					fprintf(f_boundary_2_slope, "\t\t\t(%d\t%d\t%d\t%d\t)\t\t// %d\n",
						ind[i * ncols + j], ind[i * ncols + j - 1], ind[(i - 1) * ncols + j - 1], ind[(i - 1) * ncols + j], n_slope);
					n_slope++;
			}
			if ((i - 1 >= 0) && (j - 1 >= 0) &&
				(((j - 2 < 0) && (bl_cond[(i - 1) * (ncols - 1) + j - 1] == 1)) ||
				 ((j - 2 >= 0) && (bl_cond[(i - 1) * (ncols - 1) + j - 1] * bl_cond[(i - 1) * (ncols - 1) + j - 2] < 0)))) {
					if (bl_cond[(i - 1) * (ncols - 1) + j - 1] == 1) {
						fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d\t)\t\t// %d\n",
							ind[i * ncols + j - 1], ind[i * ncols + j - 1] + 1, ind[(i - 1) * ncols + j - 1] + 1,
							ind[(i - 1) * ncols + j - 1], n_side);
						n_side++;
					} else {
						fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d\t)\t\t// %d\n",
							ind[(i - 1) * ncols + j - 1], ind[(i - 1) * ncols + j - 1] + 1, ind[i * ncols + j - 1] + 1,
							ind[i * ncols + j - 1], n_side);
						n_side++;
					}
			}
			if ((i - 1 >= 0) && (j - 1 >= 0) &&
				(((i - 2 < 0) && (bl_cond[(i - 1) * (ncols - 1) + j - 1] == 1)) ||
				 ((i - 2 >= 0) && (bl_cond[(i - 1) * (ncols - 1) + j - 1] * bl_cond[(i - 2) * (ncols - 1) + j - 1] < 0)))) {
					if (bl_cond[(i - 1) * (ncols - 1) + j - 1] == 1) {
						fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d\t)\t\t// %d\n",
							ind[(i - 1) * ncols + j - 1], ind[(i - 1) * ncols + j - 1] + 1, ind[(i - 1) * ncols + j] + 1,
							ind[(i - 1) * ncols + j], n_side);
						n_side++;
					} else {
						fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d\t)\t\t// %d\n",
							ind[(i - 1) * ncols + j], ind[(i - 1) * ncols + j] + 1, ind[(i - 1) * ncols + j - 1] + 1,
							ind[(i - 1) * ncols + j - 1], n_side);
						n_side++;
					}
			}
			if ((i - 1 >= 0) && (j == ncols - 1) && (bl_cond[(i - 1) * (ncols - 1) + j - 1] == 1)) {
				fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d\t)\t\t// %d\n",
					ind[(i - 1) * ncols + j], ind[(i - 1) * ncols + j] + 1, ind[i * ncols + j] + 1, ind[i * ncols + j], n_side);
				n_side++;
			}
			if ((j - 1 >=0) && (i == nrows - 1) && (bl_cond[(i - 1) * (ncols - 1) + j - 1] == 1)) {
				fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d\t)\t\t// %d\n",
					ind[i * ncols + j], ind[i * ncols + j] + 1, ind[i * ncols + j - 1] + 1, ind[i * ncols + j - 1], n_side);
				n_side++;
			}
		}
	}

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

	int n_z_level = (max_z - min_z) / cellsize + 1;
	int *ind_z_level;
	ind_z_level = (int *) malloc(ncols * nrows * sizeof(int));
	for (i = 0; i < ncols * nrows; i++) {
		if (mass[i] != nodata_value)
			ind_z_level[i] = (mass[i] - min_z) / cellsize;
		else
			ind_z_level[i] = -1;
	}
	float *sumx = (float *) malloc(n_z_level * sizeof(float));
	float *sumy = (float *) malloc(n_z_level * sizeof(float));
	float *sumxy = (float *) malloc(n_z_level * sizeof(float));
	float *sumx2 = (float *) malloc(n_z_level * sizeof(float));
	float *app_a = (float *) malloc(n_z_level * sizeof(float));
	float *app_b = (float *) malloc(n_z_level * sizeof(float));
	float *app_n = (float *) malloc(n_z_level * sizeof(float));
	float *kv_otkl = (float *) malloc(n_z_level * sizeof(float));
	float *x_center = (float *) malloc(n_z_level * sizeof(float));
	float *y_center = (float *) malloc(n_z_level * sizeof(float));
	float *a_center = (float *) malloc(n_z_level * sizeof(float));
	float *b_center = (float *) malloc(n_z_level * sizeof(float));
	float *flag_x = (float *) malloc(n_z_level * sizeof(float));
	float *max_otkl = (float *) malloc(n_z_level * sizeof(float));
	float *snow_depth = (float *) malloc(ncols * nrows * sizeof(float));
	for (k = 0; k < n_z_level; k++) {
		sumx[k] = sumy[k] = sumxy[k] = sumx2[k] = app_n[k] = x_center[k] = y_center[k] = flag_x[k] = 0;
		for (i = 0; i < nrows; i++) {
			for (j = 0; j < ncols; j++) {
				if (ind_z_level[i * ncols + j] == k) {
					app_n[k] = app_n[k] + 1;
					sumx[k] = sumx[k] + cellsize * i;
					sumy[k] = sumy[k] + cellsize * j;
					sumxy[k] = sumxy[k] + cellsize * cellsize * i * j;
					sumx2[k] = sumx2[k] + cellsize * cellsize * i * i;
				}
			}
		}
		if (app_n[k] != 0) {
			x_center[k] = sumx[k] / app_n[k];
			y_center[k] = sumy[k] / app_n[k];
			if (app_n[k] * sumx2[k] != sumx[k] * sumx[k])
				app_a[k] = (app_n[k] * sumxy[k] - sumx[k] * sumy[k]) / (app_n[k] * sumx2[k] - sumx[k] * sumx[k]);
			else
				flag_x[k] = 1;
			if (flag_x[k] == 0)
				app_b[k] = (sumy[k] - app_a[k] * sumx[k]) / app_n[k];
			else
				app_b[k] = sumx[k] / app_n[k];
		}
		if (app_a[k] != 0)
			a_center[k] = 1 / app_a[k];
		else
			a_center[k] = 0;
		if (flag_x[k] == 0)
			b_center[k] = y_center[k] - a_center[k] * x_center[k];
		else
			b_center[k] = x_center[k];
		kv_otkl[k] = max_otkl[k] = 0;
		for (i = 0; i < nrows; i++) {
			for (j = 0; j < ncols; j++) {
				if (ind_z_level[i * ncols + j] == k) {
					kv_otkl[k] = kv_otkl[k] + (cellsize * j - (app_a[k] * cellsize * i + app_b[k])) *
						(cellsize * j - (app_a[k] * cellsize * i + app_b[k]));
					if (flag_x[k] == 0)
						snow_depth[i * ncols + j] =
							(cellsize * i - (cellsize * i * app_a[k] + b_center[k] - cellsize * j) / (app_a[k] - a_center[k])) *
							(cellsize * i - (cellsize * i * app_a[k] + b_center[k] - cellsize * j) / (app_a[k] - a_center[k])) +
							(cellsize * j - a_center[k] * (cellsize * i * app_a[k] + b_center[k] - cellsize * j) /
								(app_a[k] - a_center[k]) + b_center[k]) *
							(cellsize * j - a_center[k] * (cellsize * i * app_a[k] + b_center[k] - cellsize * j) /
								(app_a[k] - a_center[k]) + b_center[k]);
					else
						snow_depth[i * ncols + j] = (cellsize * i - b_center[k]) * (cellsize * i - b_center[k]);
					if (snow_depth[i * ncols + j] > max_otkl[k])
						max_otkl[k] = snow_depth[i * ncols + j];
				}
			}
		}
	}
	float max_kv_otkl = kv_otkl[0], min_kv_otkl = kv_otkl[0];
	for (i = 0; i < n_z_level; i++) {
		if (kv_otkl[i] < min_kv_otkl)
			min_kv_otkl = kv_otkl[i];
		if (kv_otkl[i] > max_kv_otkl)
			max_kv_otkl = kv_otkl[i];
	}
	for (k = 0; k < n_z_level; k ++) {
		for (i = 0; i < nrows; i++) {
			for (j = 0; j < ncols; j++) {
				if (ind_z_level[i * ncols + j] == k) {
					if (max_kv_otkl != min_kv_otkl)
						snow_depth[i * ncols + j] = atof(argv[3]) * snow_depth[i * ncols + j] / max_otkl[k];// *
							//kv_otkl[k] / (max_kv_otkl - min_kv_otkl);
					else
						snow_depth[i * ncols + j] = atof(argv[3]) * snow_depth[i * ncols + j] / max_otkl[k];
				}
			}
		}
	}

	int *snow_region = (int *) malloc(ncols * nrows * sizeof(int));
	float xlucorner = xllcorner;
	float ylucorner = yllcorner + cellsize * nrows;
	float xlucorner1 = xllcorner1;
	float ylucorner1 = yllcorner1 + cellsize1 * nrows1;
	for (i = 0; i < nrows; i++) {
		for (j = 0; j < ncols; j++) {
			if ((xlucorner1 - xlucorner >= 0) && (ylucorner -ylucorner1 >= 0) &&
				(j >= ((int) (xlucorner1 - xlucorner)) / cellsize) && (i >= ((int) (ylucorner - ylucorner1)) / cellsize) &&
				(j < ((int) (xlucorner1 - xlucorner)) / cellsize + ncols1) && (i < ((int) (ylucorner - ylucorner1)) / cellsize + nrows1)) {
					if (mass1[(i - ((int) (ylucorner - ylucorner1)) / (int) cellsize) * ncols1 + j - ((int) (xlucorner1 - xlucorner)) / (int) cellsize] == 1)
						snow_region[i * ncols + j] = 1;
					else if (mass1[(i - ((int) (ylucorner - ylucorner1)) / (int) cellsize) * ncols1 + j - ((int) (xlucorner1 - xlucorner)) / (int) cellsize] == 0)
						snow_region[i * ncols + j] = 0;
					else
						snow_region[i * ncols + j] = -1;
			} else {
					snow_region[i * ncols + j] = -1;
			}
		}
	}

//	printf("%d\n", nrows);
//	f = fopen("mass1.txt", "w");
//	for (i = 0; i < nrows; i++) {
//		for (j = 0; j < ncols; j++) {
//			fprintf(f, "%d\t", snow_region[i * ncols + j]);
//		}
//		fprintf(f, "\n");
//	}
//	fclose(f);

	float area_of_snow_cower = 0;
	for (i = 0; i < nrows - 1; i++) {
		for (j = 0; j < ncols - 1; j++) {
			if ((bl_cond[i * (ncols - 1) + j] !=  -1) && (snow_region[i * ncols + j] == 0)) {
				area_of_snow_cower = area_of_snow_cower + sqrt(pow(mass[(i + 1) * ncols + j] - mass[i * ncols + j], 2) + pow(cellsize,2)) *
					sqrt(pow(mass[i * ncols + j + 1] - mass[i * ncols + j],2) + pow(cellsize, 2));
			}
		}
	}
	float snow_depth_simple = atof(argv[3]) / area_of_snow_cower;
	printf("snow depth = %f\n", snow_depth_simple);
	f = fopen("setFieldsDict", "w");
	fprintf(f, "FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t\"system\";\n\tobject\tsetFieldsDict;\n}\n");
	fprintf(f, "defaultFieldValues\n(\n\tvolScalarFieldValue\talpha.water\t0\n");
	fprintf(f, "\tvolScalarFieldValue\tregion\t0\n);\n");
	fprintf(f, "regions\n(\n");
	for (i = 0; i < nrows - 1; i++) {
		for (j = 0; j < ncols - 1; j++) {
			if ((bl_cond[i * (ncols - 1) + j] !=  -1) && (snow_region[i * ncols + j] == 0)) {
				fprintf(f, "rotatedBoxToCell\n{\n");
				fprintf(f, "\torigin\t(%f\t%f\t%f\t);\n", cellsize * i, cellsize * j, mass[i * ncols + j]);
				fprintf(f, "\ti\t\t(%f\t%f\t%f\t);\n", cellsize, 0., mass[(i + 1) * ncols + j] - mass[i * ncols + j]);
				fprintf(f, "\tj\t\t(%f\t%f\t%f\t);\n", 0., cellsize, mass[i * ncols + j + 1] - mass[i * ncols + j]);
				//fprintf(f, "\tk\t\t(%f\t%f\t%f\t);\n", 0., 0., snow_depth[i * ncols + j]);
				fprintf(f, "\tk\t\t(%f\t%f\t%f\t);\n", 0., 0., snow_depth_simple);
				fprintf(f, "\tfieldValues\n\t(\n\t\tvolScalarFieldValue\talpha.water\t1\n\t);\n}\n");
			}
			if ((bl_cond[i * (ncols - 1) + j] !=  -1) && (snow_region[i * ncols + j] == 1)) {
				fprintf(f, "rotatedBoxToCell\n{\n");
				fprintf(f, "\torigin\t(%f\t%f\t%f\t);\n", cellsize * i, cellsize * j, mass[i * ncols + j]);
				fprintf(f, "\ti\t\t(%f\t%f\t%f\t);\n", cellsize, 0., mass[(i + 1) * ncols + j] - mass[i * ncols + j]);
				fprintf(f, "\tj\t\t(%f\t%f\t%f\t);\n", 0., cellsize, mass[i * ncols + j + 1] - mass[i * ncols + j]);
				fprintf(f, "\tk\t\t(%f\t%f\t%f\t);\n", 0., 0., 20.);
				fprintf(f, "\tfieldValues\n\t(\n\t\tvolScalarFieldValue\tregion\t1\n\t);\n}\n");
			}
		}
	}
	fprintf(f, ");\n");
	fclose(f);

	free(mass1);
	free(snow_region);
	free(max_otkl);
	free(flag_x);
	free(b_center);
	free(a_center);
	free(y_center);
	free(x_center);
	free(kv_otkl);
	free(app_n);
	free(app_b);
	free(app_a);
	free(sumx2);
	free(sumxy);
	free(sumy);
	free(sumx);
	free(ind_z_level);
	free(mass);
	free(ind);

	return 0;

exit:
	free(mass);
	free(mass1);
	free(ind);
	free(bl_cond);
err_file:
	fclose(f);
	fclose(f1);
	printf("Error file\n");
exit_without_massives:
	printf("asc2dicts [map in ascii format] [divided times] [volume of avalanche] [region map ascii]\n");
	return 1;
}
