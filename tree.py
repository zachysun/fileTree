import os
import argparse
from fpdf import FPDF

CODE_EXTENSIONS = ['.py', '.cpp', '.c', '.java', '.js',
                   '.ts', '.html', '.css', '.sql', '.sh',
                   '.cu', '.rs', '.vue']


def parse_args():
    parser = argparse.ArgumentParser(description='A simple Python script:'
                                                 '(1)Customizes to output the structure of project files. '
                                                 '(2)Concatenates the code in the project files into one PDF document.')
    parser.add_argument('--directory', default='.',
                        help='Directory to start the tree from. Defaults to the current directory.')
    parser.add_argument('--if-merge', action='store_true',
                        help='Whether to merge code files into a single document.')
    parser.add_argument('--merge-type', default='txt', choices=['txt', 'pdf'],
                        help='The type of document to merge code files into. Choices are txt or pdf. Default is txt.')
    parser.add_argument('--n', type=int, default=10,
                        help='Limit on the number of items to display from each directory. '
                             'Displays only the first 3 if more than n.')
    parser.add_argument('--ignore', nargs='*',
                        default=['.git', '.idea', '__pycache__', '.gitignore', 'LICENSE',
                                 'node_modules', '.DS_Store'],
                        help='List of filenames or directories to ignore. '
                             'Default is [".git", ".idea", "__pycache__", ".gitignore", "LICENSE", '
                             '"node_modules", ".DS_Store"]')
    parser.add_argument('--specific-ext', nargs='*', default=[],
                        help='List of specific file extensions to include.')
    parser.add_argument('--nonspecific-ext', nargs='*', default=[],
                        help='List of file extensions to exclude.')
    parser.add_argument('--max-depth', type=int, default=None,
                        help='Maximum depth of directories to traverse.')
    return parser.parse_args()


def generate_file_tree(directory, depth=0, max_depth=None, n=None, ignore=None,
                       specific_ext=None, nonspecific_ext=None,
                       is_root=True):
    ignore = ignore if ignore else []
    specific_ext = specific_ext if specific_ext else []
    nonspecific_ext = nonspecific_ext if nonspecific_ext else []

    def to_ignore(file):
        file_ext = os.path.splitext(file)[1]
        if file in ignore or file_ext in nonspecific_ext:
            return True
        if specific_ext and file_ext not in specific_ext and not os.path.isdir(os.path.join(directory, file)):
            return True
        return False

    items = sorted([item for item in os.listdir(directory) if not to_ignore(item)], key=str.lower)

    lines = []
    for i, item in enumerate(items):
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            if not max_depth or depth < max_depth - 1:
                child_items = generate_file_tree(path, depth + 1, max_depth, n, ignore,
                                                 specific_ext, nonspecific_ext,
                                                 False)
                if child_items:
                    lines.append("│   " * depth + "├── " + item)
                    lines.extend(child_items)
        else:
            lines.append("│   " * depth + "├── " + item)

        if not is_root and n and len(lines) > n:
            return lines[:3] + ["│   " * depth + "├── ..."]

    return lines


def get_code_files(directory, extensions=CODE_EXTENSIONS, max_depth=None, depth=0, ignore=None):
    ignore = ignore if ignore else []
    code_files = []

    for item in os.listdir(directory):
        if item in ignore:
            continue
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            if max_depth is None or depth < max_depth:
                code_files += get_code_files(path, extensions, max_depth, depth + 1, ignore)
        elif os.path.splitext(item)[1] in extensions:
            code_files.append(path)

    return code_files


def merge_code_files(file_paths, output_type='txt', output_path='code_merge'):
    if output_type == 'txt':
        with open(f'{output_path}.txt', 'w', encoding='utf-8') as outfile:
            for file_path in file_paths:
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(f'File: {file_path}\n\n')
                    outfile.write(infile.read())
                    outfile.write('\n\n')
    elif output_type == 'pdf':
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', size=10)
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as infile:
                pdf.write(5, f'File: {file_path}\n\n')
                for line in infile:
                    pdf.write(5, line)
                pdf.write(5, '\n\n')
        pdf.output(f'{output_path}.pdf')


def main():
    args = parse_args()
    tree_lines = generate_file_tree(directory=args.directory,
                                    max_depth=args.max_depth,
                                    n=args.n,
                                    ignore=args.ignore + ['tree.py', 'file_tree.txt', 'code_merge.txt',
                                                          'code_merge.pdf'],
                                    specific_ext=args.specific_ext,
                                    nonspecific_ext=args.nonspecific_ext)
    with open('file_tree.txt', 'w', encoding='utf-8') as tree_file:
        tree_file.write('\n'.join(tree_lines))
    if args.if_merge:
        code_files = get_code_files(directory=args.directory,
                                    max_depth=args.max_depth,
                                    ignore=args.ignore + ['tree.py', 'file_tree.txt', 'code_merge.txt',
                                                          'code_merge.pdf'])
        merge_code_files(code_files, output_type=args.merge_type)


if __name__ == "__main__":
    main()
