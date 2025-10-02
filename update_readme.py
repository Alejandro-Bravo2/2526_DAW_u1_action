import datetime
import subprocess
import re
import logging
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
import os

load_dotenv()

URL_DISCORD_WEBHOOK = os.getenv("URL_WEBHOOK")



def run_tests():
    try:
        subprocess.check_call(["pytest", "-q"])
        webhook = DiscordWebhook(url=URL_DISCORD_WEBHOOK, content='✅ Tests correctos')
        webhook.execute()
        return "✅ Tests correctos"
    except subprocess.CalledProcessError:
        webhook = DiscordWebhook(url=URL_DISCORD_WEBHOOK, content='❌ Tests fallidos')
        webhook.execute()
        return "❌ Tests fallidos"

def update_readme(status: str):

    numero_mas_alto = 1;

    with open("README.md", "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        new_lines.append(line)
        if line.strip() == "## Estado de los tests":
            new_lines.append(status + "\n")
            break


    for line in lines:
        if re.search(r'## [0-9]{1,9} Estados de los test', line):
            sub_titutlo_dividido = line.split(" ")
            if re.match(r'[0-9]{1,9}', sub_titutlo_dividido[1]):
                numero_mas_alto = int(sub_titutlo_dividido[1]) + 1


    lines.append('## ' + str(numero_mas_alto) + " Estados de los test\n")
    lines.append("**Fecha y hora en la que se realizó este test:** "+ str(datetime.datetime.now()) + "\n")
    lines.append(status+"\n")
    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(lines)


def generar_reporte():
    try:
        subprocess.run("pytest -q -v  > report.md", shell=True)
        return True
    except subprocess.run():
        logging.basicConfig(filename='criticalError.log', encoding='utf-8', level=logging.CRITICAL)
        logging.critical('Error generando report.md.')
        return False


if __name__ == "__main__":
    status = run_tests()
    update_readme(status)
    generar_reporte()
