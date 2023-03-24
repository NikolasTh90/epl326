#include <iostream>
#include <omp.h>
#include <chrono>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
#include <stdbool.h>
#include <fstream>
#include <unistd.h>
using namespace std;

void generate_all_possible_texts_helper(vector<string>& all_texts, string& current_text, string& alphabet, int index) {
    if (index == current_text.size()) {
        // Add the current text to the vector of all possible texts
        all_texts.push_back(current_text);
        return;
    }
    // Generate all possible characters for the current position in the text
    for (char c : alphabet) {
        current_text[index] = c;
        // Recursively generate all possible texts starting from the next position
        generate_all_possible_texts_helper(all_texts, current_text, alphabet, index + 1);
    }
}
vector<string> generate_all_possible_texts(int length_of_text, string alphabet) {
    vector<string> all_texts;
    if (length_of_text <= 0 || alphabet.empty()) {
        return all_texts;
    }
    // Initialize the current text to be an empty string
    string current_text(length_of_text, alphabet[0]);
    // Generate all possible texts recursively
    generate_all_possible_texts_helper(all_texts, current_text, alphabet, 0);
    return all_texts;
}


string run_openssl_hash(string text, std::vector<std::string>& parameters) {
    try {
        std::string decrypted_data = "";
        for (auto& s : parameters) {
            decrypted_data += s + " ";
        }
        decrypted_data.pop_back();
        std::string cmd = "echo " + text + " | openssl " + decrypted_data;// + " 2> /dev/null";
        char buffer[128];
        string possible_plaintext = "";
        FILE* pipe = popen(cmd.c_str(), "r");
        if (!pipe) {
            std::cerr << "Error: failed to open pipe\n";
            return "";
        }
        while (!feof(pipe)) {
            if (fgets(buffer, 128, pipe) != nullptr) {
                std::string data(buffer);
                if (data.size() > 0 && data[data.size() - 1] == '\n') {
                    data.pop_back();
                }
                if (data.size() > 0 && data[data.size() - 1] == '\r') {
                    data.pop_back();
                }
                possible_plaintext += data;
            }
        }
        int status = pclose(pipe);
        if (status == 0) {
            return possible_plaintext;
        }
    } catch (const std::exception& e) {
        // std::cerr << "Error: " << e.what() << std::endl;
    }
    return "";
}

bool string_contains_word(string text, string word){
    size_t pos = text.find(word);
    if (pos != string::npos) {
        return true;
    }
    return false;
}

void hash_bruteforce(string hash_function, int length_of_text, string digest_to_match, const char* alphabet) {
    vector<string> all_texts = generate_all_possible_texts(length_of_text, alphabet);
    vector<string> parameters = {"dgst", "-" + hash_function};
    cout << "HASH with text length " << length_of_text << " with given alphabet " << alphabet << endl;
    cout << "Digest to match: " << digest_to_match << endl;
    cout << "Start ";
    # pragma omp parallel
    {
        # pragma omp single
        {
            cout << omp_get_num_threads() << " threads." << endl;
        }
        # pragma omp for
        for (int i=0; i<all_texts.size();i++){
            // string decrypted = run_openssl_hash(all_texts.at(i), parameters);
            string decrypted = run_openssl_hash("053765860" + all_texts.at(i), parameters);
            // string decrypted = run_openssl_hash(all_texts.at(i) + "1038393", parameters);
            // string decrypted = run_openssl_hash("sadamo02" + all_texts.at(i), parameters);
            // string decrypted = run_openssl_hash(all_texts.at(i) + "sadamo02", parameters);

            if (string_contains_word(decrypted, digest_to_match))
                cout << "Text: " << all_texts.at(i) << " Digest: " << decrypted << endl;
        }
    }
    cout << "End" << endl;
    cout << "Digest to match: " << digest_to_match << endl;
    cout << "HASH with text length " << length_of_text << " with given alphabet " << alphabet << endl;

}
int main(int argc, char* argv[]){
    auto start_time = chrono::high_resolution_clock::now();
    hash_bruteforce("sha256",2,"8d97ca9275bdb4dd5f60b6978275295a82026f1d06c5bd55bbbb8f492830f3a8","0123456789");
    auto end_time = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::microseconds>(end_time - start_time);
    cout << "Execution time: " << duration.count()/(1000000.0 * 60)  << " minutes." << endl;

}               