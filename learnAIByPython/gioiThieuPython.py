import pandas

#  số chẵn hay lẻ
n = int(input("Nhap vao so N = "))

# tính điểm môn học
ho_ten = input("Nhap vao ten = ")
diem_so = float(input("Nhap vao diem so = "))
ten_mon = input("Nhap vao ten mon = ")

while (ten_mon != "toan") and (ten_mon != "van") and (ten_mon != "anh"):
    ten_mon = input("Nhap vao ten mon = ")

def print_hi(name):
    print(f'Hi, {name}')


def so_chan_le():
    if n%2==0:
        print("so chan")
    else:
        print("so le")

def diem_so_mon_hoc():
    if ten_mon=="toan":
        diem_cuoi_cung = diem_so*3
    elif ten_mon=="van":
        diem_cuoi_cung = diem_so*2
    else:
        diem_cuoi_cung = diem_so
    print("Diem cuoi cung: {}".format(diem_cuoi_cung))

if __name__ == '__main__':
    print_hi('PyCharm')
    so_chan_le()
    diem_so_mon_hoc()

