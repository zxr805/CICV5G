def main():
    input_files = ['v2v_info-01.txt', 'v2v_info-02.txt', 'v2v_info-03.txt', 'v2v_info-04.txt', 'v2v_info-05.txt']
    output_file = 'all.txt'

    with open(output_file, 'w') as output:
        for idx, file_name in enumerate(input_files):
            with open(file_name, 'r') as input_file:
                if idx == 0:
                    # 对于第一个文件，直接复制全部内容
                    output.write(input_file.read())
                else:
                    # 对于第二个和第三个文件，跳过第一行，复制其余内容
                    lines = input_file.readlines()[1:]
                    output.writelines(lines)


if __name__ == '__main__':
    main()
