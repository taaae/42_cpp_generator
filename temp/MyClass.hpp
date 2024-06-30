#pragma once

class MyClass {
 public:
  MyClass();
  MyClass(const MyClass& other);
  MyClass& operator=(const MyClass& other);
  ~MyClass();
};
