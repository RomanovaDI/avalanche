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

	ind = 0;
	for (k = 0; k < kz - 1; k++) {
		for (i = 0; i < ky - 1; i++) {
			for (j = 0; j < kx - 1; j++) {
				fprintf(f_blocks, "\thex (%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t)\t(%d\t%d\t%d\t) simpleGrading (1 1 1) // %d\n",
					k * ky * kx + i * kx + j, k * ky * kx + i * kx + j + 1, k * ky * kx + (i + 1) * kx + j + 1, k * ky * kx + (i + 1) * kx + j,
					(k + 1) * ky * kx + i * kx + j, (k + 1) * ky * kx + i * kx + j + 1, (k + 1) * ky * kx + (i + 1) * kx + j + 1, (k + 1) * ky * kx + (i + 1) * kx + j,
					atoi(argv[1]), atoi(argv[2]), atoi(argv[3]),
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
	FILE *f = fopen("blockMeshDict", "w");
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


	return 0;

exit:
err_file:
	fclose(f);
	printf("Error file\n");
exit_without_massives:
error:
	printf("mkDicts30AngleSlope [kx] [ky] [kz]\n");
	return 1;
}
