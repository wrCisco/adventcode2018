#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <iterator>


int main(int argc, char *argv[])
{
  std::vector<int> recipes { 3, 7 };
  size_t cur_index1 = 0;
  size_t cur_index2 = 1;

  std::vector<int> obj { 7, 9, 3, 0, 6, 1 };

  while (recipes.size() < 6
         || !(std::equal(recipes.end() - 6, recipes.end(), obj.begin())
              || std::equal(recipes.end() - 7, recipes.end() - 1, obj.begin()))) {
    std::string new_recipes_str = std::to_string(recipes[cur_index1] + recipes[cur_index2]);
    for (size_t i = 0; i < new_recipes_str.size(); ++i) {
      recipes.push_back(new_recipes_str[i] - 0x30);
    }
    cur_index1 = (cur_index1 + 1 + recipes[cur_index1]) % recipes.size();
    cur_index2 = (cur_index2 + 1 + recipes[cur_index2]) % recipes.size();

    if (recipes.size() == recipes.capacity()) {
      recipes.reserve(recipes.size() + 10000);
    }
    if (recipes.size() == 793071 || recipes.size() == 793072) {
      for (size_t i = 793061; i < 793071; ++i) {
        std::cout << recipes[i];
      }
      std::cout << '\n';
    }
  }

  if (std::equal(obj.begin(), obj.end(), recipes.begin() + (recipes.size() - 6))) {
    std::cout << recipes.size() - 6 << '\n';
  }
  else {
    std::cout << recipes.size() - 7 << '\n';
  }

  return 0;
}

