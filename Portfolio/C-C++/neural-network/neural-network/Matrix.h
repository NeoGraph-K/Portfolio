#pragma once

#include <cstdarg>

template <typename T>
class Matrix
{
private:
	T** __structdata__;
	unsigned int __first__, __second__;
public:
	Matrix& operator=(const Matrix& other) {
		for (unsigned int i = 0; i < __first__; ++i) {
			delete[] __structdata__[i];
		}
		delete[] __structdata__;
		__first__ = other.__first__;
		__second__ = other.__second__;
		__structdata__ = new T * [__first__];
		for (unsigned int i = 0; i < __first__; ++i) {
			__structdata__[i] = new T[__second__];
		}

		for (unsigned int i = 0; i < __first__; ++i) {
			for (unsigned int j = 0; j < __second__; ++j) {
				__structdata__[i][j] = other[i][j];
			}
		}
		return *this;
	}
	T* operator[](unsigned int index){
		return __structdata__[index];
	}
	T* operator[](unsigned int index) const {
		return __structdata__[index];
	}
	Matrix operator*(double arg) {
		Matrix result(*this);
		for (unsigned int i = 0; i < result.__first__; ++i) {
			for (unsigned int j = 0; j < result.__second__; ++j) {
				result[i][j] = result[i][j] * arg;
			}
		}
		return result;
	}
public:
	void Set(int begin, ...) {
		va_list pointer;
		va_start(pointer, begin);
		__structdata__[0][0] = begin;
		for (unsigned int i = 0; i < __first__; ++i) {
			for (unsigned int j = 0; j < __second__; ++j) {
				if (j == 0 && i == 0) continue;
				__structdata__[i][j] = va_arg(pointer, T);
			}
		}
		va_end(pointer);
	}
public:
	Matrix(unsigned int first = 4, unsigned int second = 4)
		: __first__(first), __second__(second)
		, __structdata__(nullptr)
	{
		__structdata__ = new T * [__first__];
		for (unsigned int i = 0; i < __first__; ++i) {
			__structdata__[i] = new T[__second__];
		}

		for (unsigned int i = 0; i < __first__; ++i) {
			for (unsigned int j = 0; j < __second__; ++j) {
				__structdata__[i][j] = T();
			}
		}
	}
	Matrix(const Matrix& other)
		: __first__(other.__first__), __second__(other.__second__)
		, __structdata__(nullptr)
	{
		__structdata__ = new T * [__first__];
		for (unsigned int i = 0; i < __first__; ++i) {
			__structdata__[i] = new T[__second__];
		}

		for (unsigned int i = 0; i < __first__; ++i) {
			for (unsigned int j = 0; j < __second__; ++j) {
				__structdata__[i][j] = other[i][j];
			}
		}
	}
	Matrix(const Matrix&& other)
		: __first__(other.__first__), __second__(other.__second__)
		, __structdata__(nullptr)
	{
		__structdata__ = new T * [__first__];
		for (unsigned int i = 0; i < __first__; ++i) {
			__structdata__[i] = new T[__second__];
		}

		for (unsigned int i = 0; i < __first__; ++i) {
			for (unsigned int j = 0; j < __second__; ++j) {
				__structdata__[i][j] = other[i][j];
			}
		}
	}
	~Matrix() {
		for (unsigned int i = 0; i < __first__; ++i) {
			delete[] __structdata__[i];
		}
		delete[] __structdata__;
	}
};