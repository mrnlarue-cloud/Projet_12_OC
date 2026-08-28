from epic_events.security.mot_de_passe import hash_mdp, verification_mdp

# ================================ #
# Tests de gestions des mots de passe
# ================================ #


def test_hash_different_du_mdp():
    # Création du hash du MDP
    mdp = "MotDePasse333"
    mdp_hash = hash_mdp(mdp)

    # Vérification absente mdp en clair
    assert mdp_hash != mdp


def test_verification_mdp_correct():
    # Création du hash du MDP
    mdp = "MotDePasse333"
    mdp_hash = hash_mdp(mdp)

    # Vérification acceptation MDP
    assert verification_mdp(mdp_hash, mdp) is True


def test_verification_mdp_incorrect():
    # Création du hash du bon MDP
    mdp_hash = hash_mdp("MotDePasse333")

    # Vérification refus mauvais MDP
    assert verification_mdp(mdp_hash, "MauvaisMDP") is False


def test_sel_aleatoire():
    # Création de deux hash à partir du même MDP
    mdp = "MotDePasse333"
    premier_hash = hash_mdp(mdp)
    second_hash = hash_mdp(mdp)

    # Vérification de deux hash différents
    assert premier_hash != second_hash
