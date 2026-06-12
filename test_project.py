import pytest
from project import stud , grp_size , display_stud , binomials , near_certain


# https://stackoverflow.com/questions/35851323/how-to-test-a-function-with-input-call
def test_stud(monkeypatch):

    # Define user input sequence
    usr_inpts = iter([2, 26 , "s" , 2 , 150 , 150 ,
    10 , 10, "100 , 50 , 0 , 0" , "150 , 0 , 0 , 0" ,
    "0 , 0 , 10" , "0,10,0"])

    # reassign the built-in input function to assign items from that iterator sequence sequentially
    monkeypatch.setattr("builtins.input" , lambda _: next(usr_inpts))

    # execute and verify
    result = stud()
    assert result == {26: 250 , 27 : 60 , 28 : 10 , 29 : 0}

def test_grp_size(monkeypatch):

    #define user input seq
    usr_inpts = iter([10 , 5 , "t" , "," , 78 , 150 , "z"])

    # reassign the built-in input function to assign items from that iterator sequence sequentially
    monkeypatch.setattr("builtins.input" , lambda _: next(usr_inpts))

    #execute and verify
    result = grp_size(4400)
    assert result == [10 , 5 , 78 , 150]

def test_display_stud():
    sample_pop = {
        26 : 200 ,
        27 : 100 ,
        28 : 0   ,
        29 : 0
    }

    cdts_rem = sum(sample_pop.values())

    assert cdts_rem == 300

# [p_none], [p_at_least_one[] , [p_all]
@pytest.mark.parametrize("g , c , corps, expected" , [
    ([3 , 5 , 10] , 200 , 4400 , ({3: 0.87 , 5: 0.792 , 10: 0.628} , {3: 0.13 , 5: 0.208 , 10: 0.372} , {3: 0.0 , 5: 0.0 , 10: 0.0}))])

def test_binomials(g , c , corps, expected):
   assert binomials(g , c ,corps) == expected


@pytest.mark.parametrize("c , corps , expected99 , expected50", [
    (200 , 4400 , 198 , 15),
    (100 , 4400 , 401 , 31),
    (350 , 4400 , 112 , 9 )
])

def test_near_certain(c , corps, expected99 , expected50):
    assert near_certain(c , corps) == [expected99 , expected50]
