import re
class Line:
    no=0
    def __init__(self, content):
        self.content=content
        self._cursor=0
        self.lineno=Line.no
        Line.no+=1


    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self,value):
        if  value > len(self.content):
            self._cursor=len(self.content)
        elif value < 0:
            self._cursor=0
        else:
            self._cursor=value

    def cursor_increase(self, times=1):
        self.cursor += times

    def cursor_decrease(self, times=1):
        self.cursor -=times
    def __str__(self):
        return self.content
    def __repr__(self):
        return str(self.detail())

    def detail(self):
        return f"{self.lineno}: {self.content[0:self.cursor]}-{self.content[self.cursor:]}"
    def search(self,text):
        size=len(text)
        maximum=self.content-size
        while self.cursor != maximum:
            if self.content[self.cursor:self.cursor+size] != text:
                self.cursor_increase()
    def write(self, text):
        if "\n" in text:
            raise Exception("a line cannot contain \\n")
        x=self.cursor
        self.content=str(
            self.content[0:x]
            + text
            + self.content[x:]
        )
        self.cursor += len(text)

class Buffer:
    cursor=0
    def __init__(self, filepath):
        self.filepath = filepath
        self._cursor=0
        self.lines=[]

    @property
    def selectedline(self):
        return self.lines[self.cursor]

    @selectedline.setter
    def selectedline(self,text=None):
        if text:
            self.lines[self.cursor]=Line(text)
        return self.lines[self.cursor]

    @property
    def count(self):
        return len(self.lines)

    @property
    def cursor(self):
        return self._cursor


    @cursor.setter
    def cursor(self,value):
        if value < 0:
            self._cursor=0
        elif value >= self.count:
            self._cursor=self.count-1
        else:
            self._cursor = value

    def cursor_increase(self, times=1):
        self.cursor = self.cursor + times

    def cursor_decrease(self, times=1):
        self.cursor = self.cursor - times


    def open(self):
        with open(self.filepath,"r") as f:
            for text in f.readlines():
                line=Line(text)
                self.lines.append(line)
        return self


    def save(self):
        with open(self.filepath,"w") as f:
            texts=[line.content for line in self.lines]
            f.writelines(texts)

    def quit(self):
        pass

    def search(self, value, reverse=False):
        sm = re.compile(value)
        match = False
        while self.cursor < self.count-1 and self.cursor >=0:
            if reverse:
                self.cursor_decrease(times=1)

            match = sm.match(str(self.selectedline))
            if match:
                break

            if not reverse:
                self.cursor_increase(times=1)



    def openline(self):
        self.lines.append(Line(self.lines[-1]))
        for i in reversed(range(self.cursor,self.count-1)):
            self.lines[i+1] = self.lines[i]
        self.lines[self.cursor]=Line("\n")

    def deleteline(self):
        for i in range(self.cursor,self.count-1):
            self.lines[i] = self.lines[i+1]
        self.lines.pop()

    def write(self,text):
        remains=text.split("\n")
        for remained_item in remains[:-1]:
            self.selectedline.write(remained_item)
            self.cursor_increase()
            self.openline()
        self.selectedline.write(remains[-1])


class Edit:
    def __init__(self, filepath):
        self.filepath = filepath
        self.buffer=Buffer(filepath)

    def __enter__(self):
        self.buffer.open()
        return self.buffer

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.buffer.save()
        self.buffer.quit()
