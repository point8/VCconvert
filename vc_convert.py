#!/usr/bin/env python3

import re
import os
import shutil
import sys

def fix_multiline_field(vcard, field):
    s1 = re.search(r'^{}:.*'.format(field), vcard, flags=re.M)
    fixed_string = vcard
    if s1 is not None:
        s2 = re.search(r'^[A-Z;]*:.*', vcard[s1.end() + 1:], flags=re.M)
        note_string = vcard[s1.start():s1.end() + s2.start()].replace('\n', r'\n')
        fixed_string = vcard[0:s1.start()] + note_string + vcard[s1.end() + s2.start():]
    return fixed_string

def fix_vcard(filename):
    with open(filename, 'r') as myfile:
        vcard = myfile.read()
        fixed_note_string = fix_multiline_field(vcard, 'NOTE')
        fixed_org_string = fix_multiline_field(fixed_note_string, 'ORG')
        fixed_phone_string = re.sub(r'^([A-Z;]*):00', r'\1:+', fixed_org_string, flags=re.M)
        s_fax = re.search(r'^[A-Z;]*:\+49\s*$', fixed_phone_string, flags=re.M)
        fixed_fax_string = fixed_phone_string
        while s_fax is not None:
            fixed_fax_string = fixed_fax_string[0:s_fax.start()] + fixed_fax_string[s_fax.end()+1:]
            s_fax = re.search(r'^[A-Z;]*:\+49\s*$', fixed_fax_string, flags=re.M)
        return fixed_fax_string


def vc_convert(filename):
    # filename = 'Dennis_Metz.vcf'
    try:
        fixed_vcard = fix_vcard(filename)
        try:
            os.mkdir('unmodified')
        except FileExistsError:
            pass
        backup_file = os.path.join('unmodified', os.path.basename(filename))
        if not os.path.exists(backup_file):
            shutil.move(filename, backup_file)
            with open(filename, "w") as text_file:
                text_file.write(fixed_vcard)
        else:
            print('ERROR: Backup file {} already existing! '
                  'Will not overwrite...'.format(backup_file))
    except Exception:
        print('ERROR: Cannot process {}'.format(filename))
        raise


if __name__ == "__main__":
    for file in sys.argv[1:]:
        vc_convert(file)

