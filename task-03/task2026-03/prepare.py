from pathlib import Path
from zipfile import ZipFile

# подготовка данных для обучения - удаление файлов с разрывными сущностями

base = Path(__file__).parent
archive_path = base / 'NEREL-v1.1.zip'
data_dir = base / 'NEREL-v1.1'

if not archive_path.is_file():
    raise FileNotFoundError(f'Не найден архив: {archive_path}')
if data_dir.exists():
    raise FileExistsError(f'Папка {data_dir} уже существует.')

with ZipFile(archive_path) as archive:
    names = set(archive.namelist())
    for split in ('train', 'dev'):
        kept = 0
        removed = 0
        for name in sorted(names):
            if not (name.startswith(split + '/') and name.endswith('.txt')):
                continue
            ann_name = name[:-4] + '.ann'
            ann = archive.read(ann_name).decode('utf-8')
            has_discontinuous = any(
                line.startswith('T') and ';' in line.split('\t')[1]
                for line in ann.splitlines()
            )
            if has_discontinuous:
                removed += 1
                continue

            out_dir = data_dir / split
            out_dir.mkdir(parents=True, exist_ok=True)
            stem = Path(name).stem
            (out_dir / (stem + '.txt')).write_bytes(archive.read(name))
            (out_dir / (stem + '.ann')).write_bytes(archive.read(ann_name))
            kept += 1

        print(f'{split}: оставлено {kept}, исключено {removed}')
