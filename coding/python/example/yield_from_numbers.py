def gen_number():
    for i in range(10):
        yield i


def yield_from_numbers(iterators):    
    # 返回生成器 it 所產生的所有值
    yield from iterators


if __name__ == '__main__':
    gen_numbers = gen_number()
    numbers = yield_from_numbers(gen_numbers)
    for num in numbers:
        print(num)

