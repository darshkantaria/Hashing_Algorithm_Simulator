# Hashing_Algorithm_Simulator
The Hashing Algorithm Simulator is an interactive tool designed to educate users about different hashing techniques used in computer science. This simulator implements three distinct hashing algorithms: Extendible Hashing, Linear Hashing, and Bitmap Hashing. 


## Features

- **Extendible Hashing**: Demonstrates dynamic bucket splitting and keeps track of global and local depths.
- **Linear Hashing**: Simulates the process of linear hashing with a configurable load factor.
- **Bitmap Hashing**: Allows for visualization of keys using a bitmap representation.
- **Interactive User Interface**: Built with Streamlit, providing an easy-to-use interface for inserting and deleting keys.

## Getting Started

To run this project locally, follow these steps:

1. **Clone the repository**.
2. **Install required packages** (Streamlit and other dependencies).
3. **Run the Streamlit app**.
4. **Open your web browser** and navigate to the specified address to see the app in action.

## Usage

1. Select a hashing method from the sidebar: **Extendible Hashing**, **Linear Hashing**, or **Bitmap Hashing**.
2. For **Linear Hashing**, you can set the load factor threshold.
3. For **Bitmap Hashing**, specify the bitmap size.
4. Insert and delete keys as needed and observe the state of the hashing structure in real time.
5. View the internal buckets and bitmap history using the provided buttons.

## Classes Overview

- **HashingAlgorithm**: Base class for all hashing algorithms containing common functionalities.
- **ExtendibleHashing**: Implements extendible hashing with methods for insertion, deletion, and splitting of buckets.
- **LinearHashing**: Implements linear hashing with methods for insertion, deletion, and splitting based on a load factor.
- **BitmapHashing**: Implements bitmap hashing, providing functionality to manage keys using a bitmap representation.

![Screenshot 2024-10-15 001059](https://github.com/user-attachments/assets/948d0f30-3fd1-4217-a308-352f42401cf2)


