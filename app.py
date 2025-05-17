from datasets import load_dataset


def main():
    # Please pick one among the available configs: ['2023_all', '2023_level1', '2023_level2', '2023_level3']
    gaia_dataset = load_dataset('gaia-benchmark/GAIA', '2023_level1')
    
    for entry in gaia_dataset['validation']:
        print(entry)

    


if __name__ == '__main__':
    main()
