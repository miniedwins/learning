def gen_opener():
    with open("demo.log") as fd:
        yield fd


def yield_from_opener(iterators):
    for it in iterators:    	
        # yield from 語句，它將 yield 操作代理到父生成器上去。 
        # yield from it 簡單的返回生成器 it 所產生的所有值
        yield from it 


if __name__ == '__main__':
    gen_file_lines = gen_opener()
    lines = yield_from_opener(gen_file_lines)

    # 呼叫後或取得來自 gen_opener()函數的產生器
    for line in lines: 
        print(line)
