import mysql.connector

BLOCK_PREFIX = 'PSZI_AA_BLOCK'


def get_connection():
    db = mysql.connector.connect(
        host="172.30.252.36",
        user="root",
        password="ydfas67FDASdf67tgfs",
        database="pdf_signatures"
    )
    return db


def load_prev_block() -> str:
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        'SELECT id, signature FROM pdf_signatures ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    if row is not None:
        block_id, signature = row
        return f'{BLOCK_PREFIX};{block_id};{signature}'
    else:
        return f'{BLOCK_PREFIX};{0};{BLOCK_PREFIX.encode("utf8").hex()}'


def load_block(block_id: str) -> str:
    if block_id == '0':
        return f'{BLOCK_PREFIX};{0};{BLOCK_PREFIX.encode("utf8").hex()}'
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(
        'SELECT signature FROM pdf_signatures WHERE id = %s', (block_id,))
    row = cursor.fetchone()
    if row is not None:
        signature, = row
        return f'{BLOCK_PREFIX};{block_id};{signature}'
    else:
        raise Exception(f'No block with id {block_id}')


def save_new_block(sig: str):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('INSERT INTO pdf_signatures(signature) VALUES (%s)', (sig,))
    db.commit()


def admin_all():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('SELECT id, signature FROM pdf_signatures')
    return cursor.fetchall()
