#include <bits/stdc++.h>
using namespace std;
int fib_seq(int n) {
	if (n == 0) {
		return 0;
	}
	else if (n == 1) {
		return 1;
	}
	else {
		return fib_seq(n - 1) + fib_seq(n - 2);
	}
}
int main() {
	for(int i = 0; i < 10; i += 1) {
		auto x = fib_seq(i);
		cout << x << endl;
	}
	vector<string> l = {"a","b","c","d","e","f","g","h","i","j"};
	for(auto i : l) {
		cout << i << endl;
	}
	vector<vector<int>> a = {{1,2,3},{4,5,6},{7,8,9}};
	return 0;
}
