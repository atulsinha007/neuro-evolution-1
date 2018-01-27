#include <bits/stdc++.h>
using namespace std;

#define N 7
void apriori_algo( int ar [][N],int trans_size, float min_sup){
	map < set <int> , int> cand_set, el_set;
	
	for( i = 0; i < trans_size; i++){
		for ( j = 0; j < N; j++){
			if(ar[i][j]){
				set<int> new_set;
				new_set.insert(j);
				if ( el_set.find(new_set) == el_set.end()){
					el_set[new_set] = ar[i][j];
				}
				else{
					el_set[j]+=ar[i][j];
				}
			}
		}

	}
	


}
int main(){

}