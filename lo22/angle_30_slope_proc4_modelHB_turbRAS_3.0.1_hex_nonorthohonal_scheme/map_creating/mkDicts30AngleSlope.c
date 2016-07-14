#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>

/*	mkDicts30AngleSlope [kx] [ky] [kz]	*/

int main(int argc, char **argv)
{
	if (argc != 4) {
		printf("Error arguments\n");
		goto error;
	}

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

	float cellsize = 5;
	int i, j, k, kx = 200 + 1, ky = 100 + 1, kz = 4 + 1, ind = 0;
	for (k = 0; k < kz; k++) {
		for (i = 0; i < ky; i++) {
			for (j = 0; j < kx; j++) {
				fprintf(f_vertices, "\t(%f\t%f\t%f\t)\t\t// %d\n",
						j * cellsize, i * cellsize, -0.577 * j * cellsize + 577, ind);
				ind++;
				}
			}
		}
	}

	ind = 0;
	for (k = 0; k < kz - 1; k++) {
		for (i = 0; i < ky - 1; i++) {
			for (j = 0; j < kx - 1; j++) {
				fprintf(f_blocks, "\thex (%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t)\t(%d\t%d\t%d\t) simpleGrading (1 1 1) // %d\n",
					k * ky * kx + i * kx + j, k * ky * kx + i * kx + j + 1, k * ky * kx + (i + 1) * kx + j + 1, k * ky * kx + (i + 1) * kx + j,
					(k + 1) * ky * kx + i * kx + j, (k + 1) * ky * kx + i * kx + j + 1, (k + 1) * ky * kx + (i + 1) * kx + j + 1, (k + 1) * ky * kx + (i + 1) * kx + j,
					ind);
				ind++;
				if (k == kz - 2)
					fprintf(f_boundary_3_atmosphere, "\t\t\t(%d\t%d\t%d\t%d)\t\t//  \n",
						(k + 1) * ky * kx + i * kx + j, (k + 1) * ky * kx + i * kx + j + 1,
						(k + 1) * ky * kx + (i + 1) * kx + j + 1, (k + 1) * ky * kx + (i + 1) * kx + j);
				if (k == 0)
					fprintf(f_boundary_2_slope, "\t\t\t(%d\t%d\t%d\t%d)\t\t// \n",
						k * ky * kx + i * kx + j, k * ky * kx + (i + 1) * kx + j, k * ky * kx + (i + 1) * kx + j + 1, k * ky * kx + i * kx + j + 1);
				if (i == 0)
					fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\t\t// \n",
						k * ky * kx + i * kx + j, k * ky * kx + i * kx + j + 1, (k + 1) * ky * kx + i * kx + j + 1, (k + 1) * ky * kx + i * kx + j);
				if (i == ky - 2)
					fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\t\t// \n",
						k * ky * kx + i * kx + j, (k + 1) * ky * kx + i * kx + j, (k + 1) * ky * kx + i * kx + j + 1, k * ky * kx + i * kx + j + 1);
				if (j == 0)
					fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\t\t// \n",
						k * ky * kx + i * kx + j, k * ky * kx + i * kx + j + 1, (k + 1) * ky * kx + i * kx + j + 1, (k + 1) * ky * kx + i * kx + j);
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
	printf("mkDicts30AngleSlope [kx] [ky] [kz]\n");
	return 1;
}
