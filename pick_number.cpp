#include <iostream>
#include <stack>
#include <queue>
using namespace std;

#define DUMMY_STRING "DUMMY_STRING"
const int RANGE = 20100;

vector<int> prime_table;
vector<string> memo(RANGE + 1, DUMMY_STRING);

// https://qiita.com/EqualL2/items/0964832dd7929d4004ad
void sieve(size_t max){
	std::vector<bool> IsPrime;
    if(max+1 > IsPrime.size()){     // resizeで要素数が減らないように
        IsPrime.resize(max+1,true); // IsPrimeに必要な要素数を確保
    }
    IsPrime[0] = false; // 0は素数ではない
    IsPrime[1] = false; // 1は素数ではない

    for(size_t i=2; i*i<=max; ++i) // 0からsqrt(max)まで調べる
        if(IsPrime[i]) // iが素数ならば
            for(size_t j=2; i*j<=max; ++j) // (max以下の)iの倍数は
                IsPrime[i*j] = false;      // 素数ではない
    for(size_t i=2; i*i<=max; ++i){
    	if(IsPrime[i])
	    	prime_table.push_back(i);
    }
}


// stack top is 0 or 1
// make 0 or N

struct State{
	stack<int> st;
	queue<char> way;
};
/*
int bfs(){
	queue<State> que;
	State answer_tmp[RANGE * 2 + 1];
	State *answer = answer_tmp + RANGE;

	State state;
	state.st.push(1);
	que.push(state);

	while(!que.empty()){
		State curr = que.front();
		que.pop();

		if(curr.st.top() > RANGE * 2 || curr.st.top() < -RANGE * 2){
			continue;
		}
		if(curr.st.size() == 1){
			if(curr.st.top() > RANGE || curr.st.top() < -RANGE){
				continue;
			}
			if(!answer[curr.st.top()].way.empty() &&
				answer[curr.st.top()].way.size() <= curr.way.size()){
				continue;
			}
			cout << curr.st.top() << " is " << curr.way.size() << " chars. ";
			cout << "que size is " << que.size() << endl;
			answer[curr.st.top()] = curr;
			if(false && answer[-curr.st.top()].way.empty()){
				auto curr_rev = curr;
				curr_rev.way.push('0');
				curr_rev.way.push('0');
				curr_rev.way.push('0');
				curr_rev.way.push('=');
				curr_rev.way.push('%');
				curr_rev.way.push('-');
				curr_rev.st.pop();
				curr_rev.st.push(-curr.st.top());
				answer[curr_rev.st.top()] = curr_rev;
			}
			if(answer[-curr.st.top() + 1].way.empty()){
				State curr_rev1;
				curr_rev1.st = curr.st;
				auto currway_clone = curr.way;
				curr_rev1.way.push('"');
				while(!currway_clone.empty()){
					curr_rev1.way.push(currway_clone.front());
					currway_clone.pop();
				}
				curr_rev1.way.push('-');
				curr_rev1.st.pop();
				curr_rev1.st.push(-curr.st.top() + 1);
				answer[-curr.st.top() + 1] = curr_rev1;
			}

			bool flag = true;
			for(int i = -RANGE; i <= RANGE; i++){
				if(answer[i].way.empty()){
					flag = false;
					break;
				}
			}
			if(flag) break;
		}

		if(curr.way.size() >= 20){
			continue;
		}

		State next_dup = curr;
		next_dup.way.push('"');
		next_dup.st.push(next_dup.st.top());
		que.push(next_dup);

		if(curr.st.size() >= 2){
			int x, y;

			State next_sub = curr;
			next_sub.way.push('-');
			y = next_sub.st.top(); next_sub.st.pop();
			x = next_sub.st.top(); next_sub.st.pop();
			next_sub.st.push(x - y);
			que.push(next_sub);

			State next_add = curr;
			next_add.way.push('+');
			y = next_add.st.top(); next_add.st.pop();
			x = next_add.st.top(); next_add.st.pop();
			next_add.st.push(x + y);
			que.push(next_add);
		}

	}

	for(int i = -RANGE; i <= RANGE; i++){
		State curr = answer[i];
		if(curr.st.empty()){
			cout << i << " is not found";
		}
		else{
			cout << i << " is " << curr.way.size() << " chars ";
		}
		while(!curr.way.empty()){
			cout << curr.way.front();
			curr.way.pop();
		}
		cout << endl;
	}

}
*/
/*
int bfs_positive(){
	queue<State> que;
	State answer[RANGE + 1];

	State state;
	state.st.push(1);
	que.push(state);

	while(!que.empty()){
		State curr = que.front();
		que.pop();

		if(curr.st.top() > RANGE * 2){
			continue;
		}
		if(curr.st.size() == 1){
			if(curr.st.top() > RANGE){
				continue;
			}
			if(!answer[curr.st.top()].way.empty() &&
				answer[curr.st.top()].way.size() <= curr.way.size()){
				continue;
			}
			cout << curr.st.top() << " is " << curr.way.size() << " chars. ";
			cout << "que size is " << que.size() << endl;
			answer[curr.st.top()] = curr;

			bool flag = true;
			for(int i = 0; i <= RANGE; i++){
				if(answer[i].way.empty()){
					flag = false;
					break;
				}
			}
			if(flag) break;

			if(curr.st.top() == 239){
				break;
			}
		}

		State next_dup = curr;
		next_dup.way.push('"');
		next_dup.st.push(next_dup.st.top());
		que.push(next_dup);

		if(curr.st.size() >= 2){
			int x, y;
			State next_add = curr;
			next_add.way.push('+');
			y = next_add.st.top(); next_add.st.pop();
			x = next_add.st.top(); next_add.st.pop();
			next_add.st.push(x + y);
			que.push(next_add);
		}

	}

	for(int i = 0; i <= RANGE; i++){
		State curr = answer[i];
		if(curr.st.empty()){
			cout << i << " is not found";
		}
		else{
			cout << i << " is " << curr.way.size() << " chars ";
		}
		while(!curr.way.empty()){
			cout << curr.way.front();
			curr.way.pop();
		}
		cout << endl;
	}

}
*/
string recur_positive_(int target, int depth = 0, bool is_1_origin = true){
	//for(int i = 0; i < depth; i++) cout << " ";
	//cout << target << endl;

	string ans = DUMMY_STRING;

	if(memo[target] != DUMMY_STRING){
		//for(int i = 0; i < depth; i++) cout << " ";
		//cout << target << "is in memo" << endl;
		return memo[target];
	}

	if(target == 0){
		ans = DUMMY_STRING;
		return ans;
	}
	if(target == 1){
		ans = "";
		return ans;
	}
	if(target % 2 == 0){
		string ans2 = recur_positive_(target / 2, depth + 1) + string("\"+");
		if(ans == DUMMY_STRING) ans = ans2;
		else ans = (ans.size() <= ans2.size()) ? ans : ans2;
	}
	else if(target % 3 == 0){
		string ans2 = recur_positive_(target / 3, depth + 1) + "\"\"++";
		if(ans == DUMMY_STRING) ans = ans2;
		else ans = (ans.size() <= ans2.size()) ? ans : ans2;
	}
	else if(target % 5 == 0){
		string ans2 = recur_positive_(target / 5, depth + 1) + "\"\"+\"++";
		if(ans == DUMMY_STRING) ans = ans2;
		else ans = (ans.size() <= ans2.size()) ? ans : ans2;
	}
	for(auto p : prime_table){
		if(p <= 5) continue;
		if(target > p && target % p == 0){
			string ans2 = recur_positive_(p, depth + 1) + '"' +
				recur_positive_(target / p - 1, depth + 1, false) + '+';
			if(ans == DUMMY_STRING) ans = ans2;
			else ans = (ans.size() <= ans2.size()) ? ans : ans2;
		}
	}
	if(ans == DUMMY_STRING){
		ans = '"' + recur_positive_(target - 1, depth + 1) + '+';
	}

	if(is_1_origin && target % 2 == 1){
		string ans2 = '"' + recur_positive_(target - 1, depth + 1) + '+';
		ans = (ans.size() <= ans2.size()) ? ans : ans2;
	}

	memo[target] = ans;

	return ans;
}

int recur_positive(int specific_number = 0){
	int begin, end;
	if(specific_number == 0){
		begin = 1;
		end = RANGE;
	}
	else{
		begin = end = specific_number;
	}

	for(int i = begin; i <= end; i++){
		auto ans = recur_positive_(i);
		cout << i << " is " << ans.size() << " chars " << ans << endl;
	}
}

int main(){
	sieve(RANGE * RANGE);
	recur_positive();
}
