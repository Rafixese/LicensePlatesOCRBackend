class LicensePlatesComparator:
    def __init__(self):
        self.aliases = {'0': ['O', 'Q', '0'],
                        'O': ['0', 'Q', 'O'],
                        'Q': ['O', '0', 'Q'],
                        'I': ['1', 'I'],
                        '1': ['I', '1']}

    def generate_similar_license_plates_strings(self, a):
        n_similar_chars = len([char for char in a if char in self.aliases.keys()])
        if n_similar_chars == 0:
            return [a]
        if n_similar_chars == 1:
            for i in range(len(a)):
                if a[i] not in self.aliases.keys():
                    continue
                similar_strings = []
                for alias in self.aliases[a[i]]:
                    temp_str = list(a)
                    temp_str[i] = alias
                    temp_str = ''.join(temp_str)
                    similar_strings.append(temp_str)
                return similar_strings
        else:
            for i in range(len(a)):
                if a[i] not in self.aliases.keys():
                    continue
                else:
                    combinations = []
                    prefixes = []
                    for alias in self.aliases[a[i]]:
                        prefixes.append(a[:i] + alias)
                    suffixes = self.generate_similar_license_plates_strings(a[i+1:])
                    for prefix in prefixes:
                        for suffix in suffixes:
                            combinations.append(prefix + suffix)
                    return combinations

    def compare_license_plates_strings(self, a, b):
        combinations = self.generate_similar_license_plates_strings(a)

        if a in combinations and b in combinations:
            return True
        else:
            return False
