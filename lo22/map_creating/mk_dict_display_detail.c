#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>

/*mk_dict_display_detail [angle] [divided times x] [divided times y] [divided times z]*/

int main(int argc, char **argv)
{
	if (argc != 5) {
		printf("Error arguments\n");
		goto exit_without_massives;
	}

	float x_length = 1000;
	float y_length = 500;
	float z_length = x_length * tan(atof(argv[1]) * 3.14 / 180.0);
	float hight = 20;
	int i, j, k;

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

	for (k = 0; k <= atoi(argv[4]); k++) {
		for (j = 0; j <= atoi(argv[3]); j++) {
			for (i = 0; i <= atoi(argv[2]); i++) {
				fprintf(f_vertices, "\t(%f\t%f\t%f\t)\n",
					x_length - i * x_length / atof(argv[2]), j * y_length / atof(argv[3]),
					(i * x_length / atof(argv[2])) * tan(atof(argv[1]) * 3.14 / 180.0) + k * hight / atof(argv[4]));
			}
		}
	}

	for (k = 0; k < atoi(argv[4]); k++) {
		for (j = 0; j < atoi(argv[3]); j++) {
			for (i = 0; i < atoi(argv[2]); i++) {
				fprintf(f_blocks, "\thex (%d %d %d %d %d %d %d %d) (1 1 1) simpleGrading (1 1 1)\n",
					k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i,					// 0
					k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + (j + 1) * (atoi(argv[2]) + 1) + i,				// 2
					k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + (j + 1) * (atoi(argv[2]) + 1) + i  + 1,			// 3
					k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i + 1,				// 1
					(k + 1) * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i,				// 4
					(k + 1) * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + (j + 1) * (atoi(argv[2]) + 1) + i,		// 6
					(k + 1) * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + (j + 1) * (atoi(argv[2]) + 1) + i + 1,	// 7
					(k + 1) * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i + 1);			// 5
			}
		}
	}

	k = atoi(argv[4]);
	for (j = 0; j < atoi(argv[3]); j++) {
		for (i = 0; i < atoi(argv[2]); i++) {
			fprintf(f_boundary_3_atmosphere, "\t\t\t(%d\t%d\t%d\t%d)\n",
				k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i,						// 4
				k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + (j + 1) * (atoi(argv[2]) + 1) + i,					// 6
				k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + (j + 1) * (atoi(argv[2]) + 1) + i + 1,				// 7
				k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i + 1);					// 5
		}
	}

	k = 0;
	for (j = 0; j < atoi(argv[3]); j++) {
		for (i = 0; i < atoi(argv[2]); i++) {
			fprintf(f_boundary_2_slope, "\t\t\t(%d\t%d\t%d\t%d)\n",
				k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i,						// 0
				k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i + 1,					// 1
				k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + (j + 1) * (atoi(argv[2]) + 1) + i + 1,				// 3
				k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + (j + 1) * (atoi(argv[2]) + 1) + i);					// 2
		}
	}

	i = 0;
	for (k = 0; k < atoi(argv[4]); k++) {
		for (j = 0; j < atoi(argv[3]); j++) {
			fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\n",
				k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i,						// 0
				k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + (j + 1) * (atoi(argv[2]) + 1) + i,					// 2
				(k + 1) * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + (j + 1) * (atoi(argv[2]) + 1) + i,			// 6
				(k + 1) * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i);					// 4
		}
	}

	i = atoi(argv[2]);
	for (k = 0; k < atoi(argv[4]); k++) {
		for (j = 0; j < atoi(argv[3]); j++) {
			fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\n",
				k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i,						// 1
				(k + 1) * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i,					// 5
				(k + 1) * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + (j + 1) * (atoi(argv[2]) + 1) + i,			// 7
				k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + (j + 1) * (atoi(argv[2]) + 1) + i);					// 3
		}
	}

	j = 0;
	for (k = 0; k < atoi(argv[4]); k++) {
		for (i = 0; i < atoi(argv[2]); i++) {
			fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\n",
				k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i,						// 0
				(k + 1) * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i,					// 4
				(k + 1) * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i + 1,				// 5
				k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i + 1);					// 1
		}
	}

	j = atoi(argv[3]);
	for (k = 0; k < atoi(argv[4]); k++) {
		for (i = 0; i < atoi(argv[2]); i++) {
			fprintf(f_boundary_1_sides, "\t\t\t(%d\t%d\t%d\t%d)\n",
				k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i,						// 2
				k * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i + 1,					// 3
				(k + 1) * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i + 1,				// 7
				(k + 1) * (atoi(argv[3]) + 1) * (atoi(argv[2]) + 1) + j * (atoi(argv[2]) + 1) + i);					// 6
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
	printf("mk_dict_display_detail [angle] [divided times x] [divided times y] [divided times z]\n");
	return 1;
}
