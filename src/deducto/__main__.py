from deducto.cli.session import run_proof_session

def main():
    try:
        run_proof_session()
    except (KeyboardInterrupt, EOFError):
        pass

if __name__ == '__main__':
    main()
