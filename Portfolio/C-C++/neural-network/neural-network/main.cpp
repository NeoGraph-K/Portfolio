#include <iostream>
#include "Matrix.h"

int main() {

	Matrix<int> A;

	A.Set(
		1,2,3,4,
		5,6,7,8,
		9,10,11,12,
		13,14,15,16
	);

	A = A * 2;
	A = A * 2;

	for (int i = 0; i < 4; ++i) {
		for (int j = 0; j < 4; ++j) {
			std::cout << A[i][j] << std::endl;
		}
	}

	return 0;
}