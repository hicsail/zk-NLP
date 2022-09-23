#ifndef __TENSOR_H
#define __TENSOR_H

#include <vector>

template <typename T> class Tensor {
public:
  std::vector<T> data_;
  std::vector<std::size_t> dims_;

  Tensor(std::vector<std::size_t> const & dims, const T& _initial) : dims_(dims) {
    std::size_t num_elemnents = 1;
    for (auto & dim : dims_) {
      num_elemnents *= dim;
    }
    data_ = std::vector<T>(num_elemnents, _initial);
  }

  Tensor(const Tensor<T>& rhs) {
    data_ = rhs.data_;
    dims_ = rhs.dims_;
  }

  virtual ~Tensor() {}

  // Operator overloading, for "standard" mathematical matrix operations                                                                                                                                                          
  Tensor<T>& operator=(const Tensor<T>& rhs) {
    if (&rhs == this)
      return *this;

    data_ = rhs.data_;
    dims_ = rhs.dims_;
  }

  // Tensor mathematical operations

  // Element-wise addition.                                                                                                                                                                                   
  Tensor<T> operator+(const Tensor<T>& rhs) {
    assert(this->dims_ == rhs.dims_);
    assert(this->data_.size() == rhs.data_.size());
    Tensor<T> result(this->dims_);
    for (std::size_t i = 0; i < result.data_.size(); i++) {
      result[i] = this->data_[i] + rhs.data_[i];
    }
    return result;
  }


  // Element-wise addition.
  Tensor<T>& operator+=(const Tensor<T>& rhs) {
    assert(this->dims_ == rhs.dims_);
    assert(this->data_.size() == rhs.data_.size());
    for (std::size_t i = 0; i < result.data_.size(); i++) {
      this->data_[i] += rhs.data_[i];
    }
    return *this;
  }

  // Element-wise subtraction.
  Tensor<T> operator-(const Tensor<T>& rhs) {
    assert(this->dims_ == rhs.dims_);
    assert(this->data_.size() == rhs.data_.size());
    Tensor<T> result(this->dims_);
    for (std::size_t i = 0; i < result.data_.size(); i++) {
      result[i] = this->data_[i] - rhs.data_[i];
    }
    return result;
  }

  // Element-wise subtraction.
  Tensor<T>& operator-=(const Tensor<T>& rhs) {
    assert(this->dims_ == rhs.dims_);
    assert(this->data_.size() == rhs.data_.size());
    for (std::size_t i = 0; i < result.data_.size(); i++) {
      this->data_[i] -= rhs.data_[i];
    }
    return *this;
  }

  // Tensor multiplication.
  // TODO:
  Tensor<T> operator*(const Tensor<T>& rhs) {
    assert()
    unsigned r1 = this->rows;
    unsigned c1 = this->cols;
    
    unsigned r2 = rhs.get_rows();
    unsigned c2 = rhs.get_cols();

    assert (this->dims_[1] == rhs.dims_[0]);
    
    Tensor<T> result(this->dims_[0], rhs.dims_[1], 0.0);

    for (unsigned i=0; i < this->dims_[0]; i++) {
      for (unsigned j=0; j< rhs.dims[1]; j++) {
        for (unsigned k=0; k < this->dims_[1]; k++) {
          result({i, j}) = result({i, j}) + ((*this)({i, k}) * rhs({k, j}));
        }
      }
    }

    return result;
  }

  Tensor<T>& operator*=(const Tensor<T>& rhs);
  // Tensor<T> transpose();

  // Matrix/scalar operations                                                                                                                                                                                                     
  Tensor<T> operator+(const T& rhs);
  Tensor<T> operator-(const T& rhs);
  Tensor<T> operator*(const T& rhs);
  Tensor<T> operator/(const T& rhs);

  // Matrix/vector operations                                                                                                                                                                                                     
  // std::vector<T> operator*(const std::vector<T>& rhs);
  // std::vector<T> diag_vec();

  // Access the individual elements                                                                                                                                                                                               
  T& operator()(std::vector<std::size_t> const & indices) {
    assert(indices.size() == dims_.size());
    std::size_t flat_index = 0;
    std::size_t dim_factor = 1;
    for (std::size_t i = indices.size() - 1; i >= 0; i--) {
      flat_index += indices[i] * dim_factor;
      dim_factor *= dims_[i];
    }
    return data_[flat_index];
  }
  const T& operator()(std::vector<std::size_t> const & indices) const{
    assert(indices.size() == dims_.size());
    std::size_t flat_index = 0;
    std::size_t dim_factor = 1;
    for (std::size_t i = indices.size() - 1; i >= 0; i--) {
      flat_index += indices[i] * dim_factor;
      dim_factor *= dims_[i];
    }
    return data_[flat_index];
  }
};

#endif
