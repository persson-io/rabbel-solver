from typing import List

import pandas as pd

word_df = pd.read_csv('lemmatization.csv')


def compare_list_to_df(word_list, df, column_name):
    """
    Compares a Python list of words to a column in a DataFrame.
    
    Parameters:
    word_list (list): A list of words to compare.
    df (pandas.DataFrame): The DataFrame containing the column to compare against.
    column_name (str): The name of the column in the DataFrame to compare against.
    
    Returns:
    pandas.DataFrame: A new DataFrame with the following columns:
        - 'word': The word from the input list.
        - 'in_df': Boolean indicating if the word is present in the DataFrame column.
        - 'df_count': The count of the word in the DataFrame column.
    """
    # Create a new DataFrame to store the comparison results
    comparison_df = pd.DataFrame({'word': word_list})
    
    # Check if the word is present in the DataFrame column
    comparison_df['in_df'] = comparison_df['word'].isin(df[column_name])
    
    # Count the occurrences of each word in the DataFrame column
    comparison_df['df_count'] = comparison_df['word'].map(df[column_name].value_counts())
    
    # Fill NaN values with 0 for words not present in the DataFrame column
    comparison_df = comparison_df.fillna({'df_count': 0})
    
    return comparison_df


def find_words(matrix: List[List[str]], max_length: int = float('inf')) -> List[str]:
    """
    Generate a list of all possible words that can be formed by traversing
    a matrix of letters, where each step must be to an adjacent letter
    and the same position cannot be used more than once.
   
    Parameters:
    matrix (List[List[str]]): A 2D matrix of letters
   
    Returns:
    List[str]: A list of all possible words that can be formed
    """
    words = set()
    rows, cols = len(matrix), len(matrix[0])
   
    def dfs(i, j, word, visited_positions):
        if i < 0 or i >= rows or j < 0 or j >= cols:
            return
        
        current_pos = (i, j)
        if current_pos in visited_positions:
            return
        
        visited_positions.add(current_pos)
        word += matrix[i][j]
        
        if len(word) > max_length:
            visited_positions.remove(current_pos)
            return
        
        if len(word) > 2:
            words.add(word.lower())
        
        # Check all 8 adjacent positions
        dfs(i-1, j, word, visited_positions)
        dfs(i-1, j+1, word, visited_positions)
        dfs(i-1, j-1, word, visited_positions)
        dfs(i+1, j, word, visited_positions)
        dfs(i+1, j+1, word, visited_positions)
        dfs(i+1, j-1, word, visited_positions)
        dfs(i, j-1, word, visited_positions)
        dfs(i, j+1, word, visited_positions)
        
        visited_positions.remove(current_pos)
    
    for i in range(rows):
        for j in range(cols):
            dfs(i, j, "", set())
    
    return list(words)


matrix = [
    ['K', 'L', 'L', 'N', 'F'],
    ['A', 'D', 'M', 'S', 'E'],
    ['R', 'V', 'B', 'S', 'P'],
    ['A', 'E', 'L', 'S', 'L'],
    ['N', 'S', 'E', 'O', 'R']
 ]

# matrix = [
#     ['D', 'A', 'E', 'A'],
#     ['I', 'A', 'O', 'K'],
#     ['A', 'R', 'D', 'Ö'],
#     ['E', 'I', 'A', 'V']
# ]

def solve_word_matrix(matrix, max_length=8):
    all_words = find_words(matrix, max_length=max_length)
    comparison_df = compare_list_to_df(all_words, word_df, 'lemma')
    matches = comparison_df.loc[comparison_df['in_df'] == True]
    column_name = 'word'
    matches[f'{column_name}_length'] = matches[column_name].str.len()
    matches = matches.sort_values(by=f'{column_name}_length', ascending=False)
    # Remove rows where any column contains 'X' or 'Y'
    # filtered_df = matches[~matches.astype(str).apply(lambda x: x.str.contains('k|ö|o', case=False)).any(axis=1)]
    word_list = matches[column_name].tolist()
    return word_list


# print(solve_word_matrix(matrix))