# Experiment 3: Text Analysis using LEX

This directory contains a sophisticated text analysis program that demonstrates advanced LEX features for processing natural language text and performing statistical analysis.

## 📋 Program Overview

### expt3a.l - Word Frequency Analyzer
**Purpose**: Analyzes text files to count word frequencies, providing insights into text content and structure.

**Features**:
- **Word Extraction**: Identifies all words in text, ignoring punctuation and numbers
- **Case Insensitive**: Converts all words to lowercase for consistent counting
- **Frequency Counting**: Tracks occurrence of each unique word
- **Alphabetical Sorting**: Displays results in alphabetical order
- **File Input**: Reads from specified input files
- **Data Structures**: Uses efficient table-based storage
- **Statistical Output**: Presents comprehensive frequency analysis

## 🎯 Key Capabilities

### Text Processing:
- Extracts words (sequences of alphabetic characters)
- Converts to lowercase for case-insensitive analysis
- Ignores numbers, punctuation, and special characters
- Handles various text formats and encodings

### Data Management:
- Maintains word frequency table with up to 1000 unique words
- Efficient lookup and insertion algorithms
- Automatic duplicate detection and counting
- Memory-efficient storage structure

### Output Features:
- Alphabetically sorted word list
- Frequency count for each word
- Professional formatting for analysis results
- Clear, readable presentation

## 🚀 How to Use

### Basic Compilation and Execution:
```powershell
# Navigate to experiment directory
cd "c:\Users\Joseph\Desktop\compiler design\expt3"

# Compile the analyzer
lex expt3a.l
gcc lex.yy.c -o analyzer.exe
```

### Run with Sample Input:
```powershell
# Use the provided sample file
.\analyzer.exe input.txt

# Or create your own text file
echo "LEX is powerful. LEX makes lexical analyzers." > test.txt
.\analyzer.exe test.txt
```

### Command Line Usage:
```powershell
# General syntax
.\analyzer.exe <input_file>

# Example with different files
.\analyzer.exe document.txt
.\analyzer.exe article.txt
.\analyzer.exe book_chapter.txt
```

## 📊 Sample Analysis

### Input File (input.txt):
```
Lex is powerful. Lex makes lexical analyzers.
Lex helps in compiler design, and lex is useful.
```

### Expected Output:
```
Word Frequency Analysis:
analyzers : 1
and : 1
compiler : 1
design : 1
helps : 1
in : 1
is : 2
lex : 3
lexical : 1
makes : 1
powerful : 1
useful : 1
```

### Analysis Insights:
- **Total unique words**: 12
- **Most frequent word**: "lex" (appears 3 times)
- **Case handling**: "Lex" and "lex" counted together
- **Punctuation ignored**: Periods and commas don't affect word extraction

## 🔧 Technical Implementation

### LEX Pattern Recognition:
```lex
[a-zA-Z]+   { 
    char temp[50]; 
    int i;
    for(i=0; yytext[i]; i++) 
        temp[i] = tolower(yytext[i]);
    temp[i] = '\0';
    insert_word(temp);
}
```

### Data Structure:
```c
struct {
    char word[50];
    int count;
} table[MAXWORDS];
```

### Core Algorithm:
1. **Word Detection**: Regular expression `[a-zA-Z]+` identifies alphabetic sequences
2. **Case Normalization**: Convert to lowercase using `tolower()`
3. **Duplicate Check**: Linear search through existing entries
4. **Insertion/Update**: Add new word or increment existing count
5. **Sorting**: Alphabetical ordering using `qsort()` and `strcmp()`

## 🧪 Testing Scenarios

### 1. Simple Text Analysis:
```powershell
# Create test file
echo "Hello world. Hello universe. World peace." > simple.txt
.\analyzer.exe simple.txt
```
**Expected**: hello(2), peace(1), universe(1), world(2)

### 2. Programming Documentation:
```powershell
# Analyze code comments
echo "/* This function calculates the sum. The function is efficient. */" > code.txt
.\analyzer.exe code.txt
```

### 3. Mixed Content:
```powershell
# Text with numbers and punctuation
echo "Version 2.0 released! Bug fixes: 15 issues resolved. Performance improved 50%." > mixed.txt
.\analyzer.exe mixed.txt
```

### 4. Large Text Files:
```powershell
# Download or create larger files for comprehensive analysis
.\analyzer.exe large_document.txt
```

## 📈 Advanced Applications

### 1. Document Analysis:
- **Research Papers**: Identify key terms and concepts
- **Literature**: Analyze writing style and vocabulary
- **Technical Documentation**: Find common terminology

### 2. Content Optimization:
- **SEO Analysis**: Identify keyword density
- **Writing Analysis**: Check vocabulary diversity
- **Readability Assessment**: Analyze word complexity

### 3. Data Mining:
- **Social Media**: Analyze trending topics
- **Customer Feedback**: Extract common themes
- **Survey Responses**: Identify frequent concerns

## 🔍 Enhancements and Modifications

### 1. Enhanced Word Processing:
```lex
# Handle hyphenated words
[a-zA-Z]+(-[a-zA-Z]+)*  { process_hyphenated_word(yytext); }

# Include apostrophes in words
[a-zA-Z]+('([ts]|re|ve|ll|d))?  { process_contraction(yytext); }
```

### 2. Statistical Enhancements:
```c
// Add total word count
int total_words = 0;

// Calculate percentages
printf("%s : %d (%.2f%%)\n", word, count, (count*100.0)/total_words);
```

### 3. Output Formats:
```c
// CSV output
printf("%s,%d\n", word, count);

// JSON output
printf("{\"%s\": %d}", word, count);
```

### 4. Filtering Options:
```c
// Minimum frequency threshold
if (count >= MIN_FREQUENCY) {
    printf("%s : %d\n", word, count);
}

// Word length filtering
if (strlen(word) >= MIN_LENGTH) {
    // Process word
}
```

## 🎓 Learning Objectives

### Text Processing Concepts:
- **Pattern Recognition**: Identifying linguistic patterns
- **Data Normalization**: Consistent data representation
- **Statistical Analysis**: Frequency distribution computation
- **Sorting Algorithms**: Alphabetical and numerical ordering

### Programming Techniques:
- **File I/O**: Reading from external files
- **String Manipulation**: Case conversion and processing
- **Data Structures**: Arrays and structures for data storage
- **Memory Management**: Efficient storage allocation

### LEX Advanced Features:
- **File Input Redirection**: Using `yyin` for file processing
- **Complex Patterns**: Multi-character pattern matching
- **C Integration**: Combining LEX with C functions
- **Error Handling**: Managing file access and memory limits

## 📊 Performance Considerations

### Limitations:
- **Maximum Words**: 1000 unique words (configurable)
- **Word Length**: 50 characters maximum per word
- **Memory Usage**: Linear growth with unique word count
- **Search Time**: O(n) for word lookup

### Optimizations:
```c
// Hash table for faster lookup
#define HASH_SIZE 101
struct word_entry *hash_table[HASH_SIZE];

// Binary search for sorted arrays
int binary_search(char *word) {
    // Implementation for O(log n) lookup
}
```

## 🔧 Troubleshooting

### Common Issues:

#### 1. File Not Found:
```
Error: Could not open file filename.txt
Solution: Check file path and permissions
```

#### 2. Memory Overflow:
```
Warning: Maximum word limit reached (1000)
Solution: Increase MAXWORDS constant
```

#### 3. Encoding Issues:
```
Problem: Special characters not recognized
Solution: Ensure input file uses standard text encoding
```

#### 4. Empty Output:
```
Problem: No words detected
Solution: Check if file contains alphabetic characters
```

## 📚 Real-World Applications

### Academic Research:
- **Corpus Linguistics**: Analyzing language patterns
- **Literature Studies**: Studying author vocabulary
- **Historical Analysis**: Examining document evolution

### Industry Applications:
- **Content Management**: SEO optimization
- **Market Research**: Analyzing customer feedback
- **Information Retrieval**: Building search indices

### Digital Humanities:
- **Text Mining**: Extracting insights from large corpora
- **Stylometry**: Author identification through style analysis
- **Cultural Studies**: Analyzing cultural documents

## 🔗 Integration Possibilities

### Database Integration:
```c
// Store results in database
void store_to_database(char *word, int count) {
    // SQL INSERT statements
}
```

### Web Interface:
```javascript
// Upload file and display results
function analyzeText(file) {
    // Call analyzer and format results
}
```

### Visualization:
```python
# Create word cloud
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Generate visualization from frequency data
```

---

This experiment demonstrates the power of LEX for real-world text analysis applications, providing valuable experience in natural language processing and data analysis techniques that are essential in modern computing applications.