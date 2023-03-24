#include <string>
#include <vector>
#include <algorithm>
#include <omp.h>
#include <stdbool.h>
#include <fstream>
#include <chrono>
#include <assert.h>
#include <unistd.h>
#include <iostream>

using namespace std;
vector<string> words;
string message = "ldygdv dsdytdzvpcdswUfrjlcpogykntpfabzeh";


std::string toLowerCase(std::string str) {
    std::transform(str.begin(), str.end(), str.begin(), [](unsigned char c){ return std::tolower(c); });
    return str;
}


vector<string> permutations(string str) {
    vector<string> permutated;
    sort(str.begin(), str.end());
    do {
        permutated.push_back(str);
    } while(next_permutation(str.begin(), str.end()));
    return permutated;
}

vector<string> permutations_vector(vector<string> vec) {
    vector<string> permutated;
    sort(vec.begin(), vec.end());
    do {
        string permutation;
        for(auto str : vec) {
            permutation += str;
        }
        permutated.push_back(permutation);
    } while(next_permutation(vec.begin(), vec.end()));
    return permutated;
}
vector<string> generate_alphabet(string message, bool useNums, bool useAll_numbers, bool useSpecials, string specific_special) {
    bool Upper = false, Lower = false, Nums = false, specials = false;
    string upper_alphabet = "", lower_alphabet = "", numbers = "", special_chars = "";
    
    for (int i = 0; i < message.length(); i++) {
        bool bool1 = false;
        bool bool2 = false;
        if (isupper(message[i])) {
            Upper = true;
            bool1 = true;
        }
        if (islower(message[i])) {
            Lower = true;
            bool2 = true;
        }
        // string::npos means that message[i] not found in numbers
        if (isdigit(message[i]) && numbers.find(message[i]) == string::npos) {
            Nums = true;
            numbers += message[i];
        }
        if (!bool1 && !bool2 && !isdigit(message[i]) && special_chars.find(message[i]) == string::npos) {
            special_chars += message[i];
            specials = true;
        }
    }

    // cout << numbers << "\n";
    // cout << special_chars << "\n";

    vector<string> alphabets_generation, all_alphabets, all_alphabets2, list2;
    string all_nums = "0123456789";

    if (Upper) {
        upper_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        alphabets_generation.push_back(upper_alphabet);
    }
    if (Lower) {
        lower_alphabet = "abcdefghijklmnopqrstuvwxyz";
        alphabets_generation.push_back(lower_alphabet);
    }

    // if want to use specific numbers comment this if
    if (Nums or useNums) { // Whether to use numbers or not
        if (useAll_numbers or numbers.size()>1) { // Put all numbers else put numbers found
            numbers = all_nums;
        }
        if (numbers.length()!=0){
            alphabets_generation.push_back(numbers); 
        }
    }


    // alphabets_generation.push_back("0123456789"); case you want to use any number you want

    if (useSpecials) {
        for (int i = 0; i < specific_special.length(); i++) {
            if (special_chars.find(specific_special[i]) == string::npos) {
                special_chars+=specific_special[i]; // add this to special_chars in order not to put 2 times the same char because find work only between 2 strings
            }
        }
    }

    // for (string special : list_specials) {
    //     cout << special << endl;
    // }

    // Permutate all special characters and add them to a vector of string called special_permutations.
    vector<string> specials_permutations;
    specials_permutations = permutations(special_chars); 
    list2 = permutations_vector(alphabets_generation);

    // for (string special : specials_permutations) {
    //     cout << special << endl;
    // }

    // for (string special : list2) {
    //     cout << special << endl;
    // }

    for (string alphabets : list2) {
        for (string  special : specials_permutations) {
            all_alphabets.push_back(special+alphabets); 
        }
    }

    for (string special : all_alphabets) {
        cout << special << endl;
    }

    return all_alphabets;
    
}

vector<string> dictionary() {
    ifstream dictionary("dictionary.txt");
    vector<string> list_of_words;
    string word;
    while (getline(dictionary, word)) {
        list_of_words.push_back(word);
    }
    dictionary.close();
    return list_of_words;
}

string decryptVigenere(vector<int> key1, string alphabet1) {
    vector<int> key = key1;
    string alphabet = alphabet1;
    string stringtodecrypt = message;
    string stringdecrypted = "";
    for (int i = 0; i < stringtodecrypt.length(); i++) {
        char character = stringtodecrypt[i];
        int position = alphabet.find(character);
        int key_pos = i % key.size();
        int newposition = (position - (key[key_pos]));
        if (newposition < 0) {
            newposition += alphabet.length();
        }
        stringdecrypted += alphabet[newposition];
    }
    
    // int detected_words = 0;
    // string word = "";
    // for (int i=0; i<=stringdecrypted.length(); i++) {
    //     if (stringdecrypted[i]==' ') { // if space found then go to next word
    //         for (int j=0;j<words.size();j++){ // check if word found in dictionary
    //             if (toLowerCase(word)==words.at(j)) {
    //                 detected_words+=1;
    //                 break;
    //             }
    //         }
    //         word="";
    //     }
    //     else {
    //         word+=stringdecrypted[i];
    //     }
    // }

    // if (detected_words>3) { // choose how much words you want in order to be print
    //     cout<<endl;
    //     cout<<"Key = ";
    //     for (int k=0; k<key.size(); k++) {
    //         cout<<key.at(k)<<" ";
    //     }
    //     cout<<endl<<"Alphabet : "<<alphabet << " ";
    //     cout<<endl<<"PlainText : "<<stringdecrypted<<endl;
    // }
    return stringdecrypted;
}

vector<int> copy(vector<int> list1) {
    vector<int> new_list;
    for (int i = 0; i < list1.size(); i++) {
        new_list.push_back(list1[i]);
    }
    return new_list;
}

vector<vector<int>> generateKeys(vector<vector<int>> keys, string alphabet) {
    vector<vector<int>> new_keys;
    if (keys.size() == 0) {
        for (int letter = 0; letter < alphabet.size(); letter++) {
            vector<int> temp;
            temp.push_back(letter);
            new_keys.push_back(temp);
        }
        return new_keys;
    }

    for (int i = 0; i < keys.size(); i++) {
        for (int letter = 0; letter < alphabet.size(); letter++) {
            vector<int> temp = copy(keys[i]);
            temp.push_back(letter);
            new_keys.push_back(temp);
        }
    }
    return new_keys;
}

string transposition_decrypt(string message, int key) {
    vector<vector<char>> message_array(key);
    int char_in_each_list = message.length() / key;
    int counter = 0, counter2 = 0;

    for (char character : message) {
        message_array[counter].push_back(character);
        counter2++;
        if (counter2 % char_in_each_list == 0) {
            counter++;
            counter2 = 0;
        }
    }

    for (auto& arr : message_array) {
        assert(!arr.empty());
    }

    vector<vector<char>> decrypt_array(char_in_each_list, vector<char>(key));

    for (int i = 0; i < char_in_each_list; i++) {
        for (int j = 0; j < key; j++) {
            decrypt_array[i][j] = message_array[j][i];
        }
    }

    for (auto& arr : decrypt_array) {
        assert(!arr.empty());
    }

    string plaintext;
    for (auto& sub_list : decrypt_array) {
        for (char character : sub_list) {
            plaintext += character;
        }
    }
    return plaintext;
}

void checkDecrypted(string stringdecrypted,vector<int> key, int transposition_key,string alphabet) {
    int detected_words = 0;
    string word = "";
    for (int i=0; i<=stringdecrypted.length(); i++) {
        if (stringdecrypted[i]==' ') { // if space found then go to next word
            for (int j=0;j<words.size();j++){ // check if word found in dictionary
                if (toLowerCase(word)==words.at(j)) {
                    detected_words+=1;
                    break;
                }
            }
            word="";
        }
        else {
            word+=stringdecrypted[i];
        }
    }

    if (detected_words>10) { // choose how much words you want in order to be print
        cout<<endl;
        cout<<"Vigenere Key = ";
        for (int k=0; k<key.size(); k++) {
            cout<<key.at(k)<<" ";
        }
        cout<<"Transposition Key = " <<transposition_key<<endl;
        cout<<endl<<"Alphabet : "<<alphabet << " ";
        cout<<endl<<"PlainText : "<<stringdecrypted<<endl;
    }
}

int main() {

    auto start_time = chrono::high_resolution_clock::now();
    vector<string> alphabets = generate_alphabet(message,true, false, false, ""); // Make all alphabets
    cout << "Alphabets Length = "<< alphabets.size() << endl; // Print alphabets size
    words=dictionary();   // read possible words from dictionary
    
    // Vector that contains all vigenere(size) keys 
    // Each vector<vector> vigenere(size) contains all keys for this size
    // Each vector<vector<vector<int>>> vigenere(size) contains all keys and for each key all integer keys 
    vector<vector<vector<int>>> keys;
    int max_key_size = 1; // Here put vigenere maximum keys
    for (int key_size=0; key_size<max_key_size; key_size++){
        // Generate all vigenere(0) keys
        if (key_size == 0){
            keys.push_back(generateKeys({},alphabets.at(0)));
        }
        // Generate all vigenere(key_size) keys by giving to function the 
        // previous vigenere(key-size-1) and generate all vigenere(key_size) keys
        // Add all vigenere(key_size) keys to keys vector
        else{
            keys.push_back(generateKeys(keys[key_size-1], alphabets.at(0)));
        }
        cout << "Vigenere" << key_size+1 <<" keys size = "<< keys.at(key_size).size() << endl;
    }

    cout<<"Start"<<endl;
    #pragma omp parallel
    {
        # pragma omp single
        {
            cout << "Threads = " <<omp_get_num_threads() << endl;
        }
        // schedule(static,alphabets.size()/omp_get_num_threads())
        #pragma omp for collapse(2) 
        for (int key_size=0;key_size<max_key_size;key_size++){ // for all keys
            for (int alphabet=0;alphabet<alphabets.size();alphabet++) {  // for all alphabets
                for (int j=0; j<keys.at(key_size).size();j++){
                    string vig_to_transposition=decryptVigenere(keys.at(key_size).at(j),alphabets.at(alphabet)); 
                    for (int transposition_key=1; transposition_key<=alphabets[0].size(); transposition_key++){
                        if (message.length() % transposition_key == 0){
                            string decrypted = transposition_decrypt(vig_to_transposition, transposition_key);
                            checkDecrypted(decrypted, keys.at(key_size).at(j),transposition_key,alphabets.at(alphabet));
                        }
                    }   
                }
            }
        }
        // #pragma omp for
        // for (int alphabet=0;alphabet<alphabets.size();alphabet++) {  // for all alphabets
        //             decryptVigenere({8,10,12},alphabets.at(alphabet)); 
        // }
    }
    cout<<"End"<<endl;
    auto end_time = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::microseconds>(end_time - start_time);
    cout << "Execution Time: " << duration.count()/(1000000.0 * 60 )<< " minutes" <<endl;
    return 0;
}




