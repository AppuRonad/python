import math
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Bank(Base):
    __tablename__ = 'banks'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    interest_rate = Column(Float, nullable=False)
    term_years = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)

    def calculate_total_and_profit(self):
        total_amount = self.amount * math.pow(1 + self.interest_rate / 100, self.term_years)
        profit = total_amount - self.amount
        return total_amount, profit

engine = create_engine('sqlite:///banks.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def get_bank_details():
    while True:
        name = input("Enter bank name (or 'done' to finish): ")
        if name.lower() == 'done':
            break
        interest_rate = float(input(f"Enter interest rate for {name} (%): "))
        term_years = int(input(f"Enter term (years) for {name}: "))
        amount = float(input(f"Enter the investment amount for {name}: "))
        bank = Bank(name=name, interest_rate=interest_rate, term_years=term_years, amount=amount)
        session.add(bank)
    session.commit()

def plot_profits(results):
    bank_names = [result['bankName'] for result in results]
    profits = [result['profit'] for result in results]

    plt.figure(figsize=(10, 5))
    plt.plot(bank_names, profits, marker='o', linestyle='-', color='skyblue', markersize=8, linewidth=2)
    plt.xlabel('Bank')
    plt.ylabel('Profit')
    plt.title('Profit Comparison for Different Banks')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    get_bank_details()
    
    banks = session.query(Bank).all()
    
    if not banks:
        print("No banks were entered.")
        return

    results = []
    for bank in banks:
        total_amount, profit = bank.calculate_total_and_profit()
        results.append({
            'bankName': bank.name,
            'interestRate': bank.interest_rate,
            'termYears': bank.term_years,
            'investmentAmount': bank.amount,
            'totalAmount': round(total_amount, 2),
            'profit': round(profit, 2)
        })

    print("\nResults:")
    for result in results:
        print(f"Bank: {result['bankName']}, Interest Rate: {result['interestRate']}%, Term: {result['termYears']} years, Investment Amount: {result['investmentAmount']}, Total Amount: {result['totalAmount']}, Profit: {result['profit']}")

    best_option = max(results, key=lambda x: x['profit'])
    print(f"\nThe best bank to invest in is {best_option['bankName']} with a profit of {best_option['profit']}.")

    plot_profits(results)

if __name__ == "__main__":
    main()
